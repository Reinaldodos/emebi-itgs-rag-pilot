import json
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf

from extraction_io import parse_arguments, write_output


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = (
    PROJECT_ROOT
    / "corpus"
    / "02_union_europeenne"
    / "2019_union_europeenne_reglement_2152_fr.pdf"
)
DOCUMENT_ID = "2019_union_europeenne_reglement_2152_fr"

HEADER_RE = re.compile(
    r"02019R2152 — FR — 10\.05\.2026 — 002\.001 — (?P<page>\d+)"
)
CHAPTER_RE = re.compile(r"CHAPITRE (?P<number>[IVXLCDM]+)")
ARTICLE_RE = re.compile(r"Article (?P<number>premier|\d+)")
ANNEX_RE = re.compile(r"ANNEXE (?P<number>[IVXLCDM]+)")
TITLE_RE = re.compile(r"TITRE(?: (?P<number>[IVXLCDM]+))?")
SECTION_RE = re.compile(r"SECTION(?: (?P<number>[IVXLCDM\d]+))?")
PARAGRAPH_RE = re.compile(r"(?P<number>[1-9]\d?)\.")
MARKER_RE = re.compile(r"[►▼][A-Z]\d*")
NOTE_RE = re.compile(r"\( (?P<number>\d+) \) (?P<text>.*)")

# Ces quatre articles n'ont pas de paragraphes numérotés. Le nombre de lignes
# de titre est propre à la mise en page observée dans ce règlement.
UNNUMBERED_ARTICLE_TITLE_LINES = {"1": 1, "4": 1, "15": 1, "19": 2}

# Les annexes V et VI commencent directement par leur texte introductif.
ANNEX_TITLE_LINE_COUNTS = {"I": 1, "II": 1, "III": 2, "IV": 3, "V": 0, "VI": 0}


def normalize_line(text: str) -> str:
    """Normalise uniquement les espaces horizontaux d'une ligne."""
    return re.sub(r"[\t \u00a0]+", " ", text.strip())


def extract_lines(pdf_path: Path) -> tuple[list[dict], dict]:
    lines: list[dict] = []
    removed_headers: list[dict] = []
    soft_hyphen_joins = 0

    with pymupdf.open(pdf_path) as document:
        page_count = document.page_count
        for page_number, page in enumerate(document, start=1):
            for raw_line in page.get_text("text").splitlines():
                text = normalize_line(raw_line)
                if not text:
                    continue

                header_match = HEADER_RE.fullmatch(text)
                if header_match and int(header_match.group("page")) == page_number:
                    removed_headers.append({"page": page_number, "text": text})
                    continue

                if lines and lines[-1]["text"].endswith("\u00ad"):
                    lines[-1]["text"] = lines[-1]["text"][:-1] + text
                    lines[-1]["page_end"] = page_number
                    soft_hyphen_joins += 1
                    continue

                lines.append(
                    {
                        "text": text,
                        "page_start": page_number,
                        "page_end": page_number,
                    }
                )

    extraction_report = {
        "page_count": page_count,
        "removed_repetitive_headers_and_footers": removed_headers,
        "soft_hyphen_joins": soft_hyphen_joins,
    }
    return lines, extraction_report


def line_range(lines: list[dict]) -> tuple[int, int]:
    return (
        min(line["page_start"] for line in lines),
        max(line["page_end"] for line in lines),
    )


def join_text(lines: list[dict]) -> str:
    return " ".join(line["text"] for line in lines).strip()


def markers_in(lines: list[dict]) -> list[dict]:
    return [
        {"marker": line["text"], "page": line["page_start"]}
        for line in lines
        if MARKER_RE.fullmatch(line["text"])
    ]


def separate_notes(lines: list[dict], article_number: str) -> tuple[list[dict], list[dict]]:
    content: list[dict] = []
    notes: list[dict] = []
    current_note: dict | None = None
    note_page: int | None = None

    for line in lines:
        note_match = NOTE_RE.fullmatch(line["text"])
        if note_match:
            if current_note is not None:
                notes.append(current_note)
            current_note = {
                "document_id": DOCUMENT_ID,
                "article": article_number,
                "note": note_match.group("number"),
                "page_start": line["page_start"],
                "page_end": line["page_end"],
                "text_parts": [note_match.group("text")],
            }
            note_page = line["page_start"]
        elif current_note is not None and line["page_start"] == note_page:
            current_note["text_parts"].append(line["text"])
            current_note["page_end"] = line["page_end"]
        else:
            if current_note is not None:
                notes.append(current_note)
                current_note = None
                note_page = None
            content.append(line)

    if current_note is not None:
        notes.append(current_note)

    for note in notes:
        note["text"] = " ".join(note.pop("text_parts")).strip()

    return content, notes


def parse_article(
    heading: dict,
    segment: list[dict],
    chapter_number: str,
    chapter_title: str,
) -> tuple[dict, list[dict]]:
    raw_number = ARTICLE_RE.fullmatch(heading["text"]).group("number")
    article_number = "1" if raw_number == "premier" else raw_number
    article_markers = markers_in(segment)
    content, notes = separate_notes(segment, article_number)
    content = [line for line in content if not MARKER_RE.fullmatch(line["text"])]

    first_paragraph_index = next(
        (
            index
            for index, line in enumerate(content)
            if PARAGRAPH_RE.fullmatch(line["text"])
        ),
        None,
    )

    paragraphs: list[dict] = []
    unnumbered_text = None

    if first_paragraph_index is not None:
        title_lines = content[:first_paragraph_index]
        paragraph_lines = content[first_paragraph_index:]
        current_paragraph: dict | None = None

        for line in paragraph_lines:
            paragraph_match = PARAGRAPH_RE.fullmatch(line["text"])
            if paragraph_match:
                if current_paragraph is not None:
                    paragraphs.append(current_paragraph)
                current_paragraph = {
                    "document_id": DOCUMENT_ID,
                    "chapter": chapter_number,
                    "article": article_number,
                    "paragraph": paragraph_match.group("number"),
                    "page_start": line["page_start"],
                    "page_end": line["page_end"],
                    "text_parts": [],
                }
            elif current_paragraph is not None:
                current_paragraph["text_parts"].append(line["text"])
                current_paragraph["page_end"] = line["page_end"]

        if current_paragraph is not None:
            paragraphs.append(current_paragraph)

        for paragraph in paragraphs:
            paragraph["text"] = " ".join(paragraph.pop("text_parts")).strip()
    else:
        title_line_count = UNNUMBERED_ARTICLE_TITLE_LINES.get(article_number, 1)
        title_lines = content[:title_line_count]
        body_lines = content[title_line_count:]
        if body_lines:
            body_page_start, body_page_end = line_range(body_lines)
            unnumbered_text = {
                "document_id": DOCUMENT_ID,
                "chapter": chapter_number,
                "article": article_number,
                "page_start": body_page_start,
                "page_end": body_page_end,
                "text": join_text(body_lines),
            }

    article_lines = [heading, *segment]
    page_start, page_end = line_range(article_lines)
    article = {
        "document_id": DOCUMENT_ID,
        "article": article_number,
        "heading": heading["text"],
        "title": join_text(title_lines),
        "chapter": {"number": chapter_number, "title": chapter_title},
        "page_start": page_start,
        "page_end": page_end,
        "paragraphs": paragraphs,
        "unnumbered_text": unnumbered_text,
        "eur_lex_markers": article_markers,
        "notes": notes,
    }
    return article, notes


def parse_annexes(lines: list[dict]) -> list[dict]:
    heading_starts = [
        index for index, line in enumerate(lines) if ANNEX_RE.fullmatch(line["text"])
    ]
    starts = [
        heading_start - 1
        if heading_start > 0
        and MARKER_RE.fullmatch(lines[heading_start - 1]["text"])
        and lines[heading_start - 1]["page_start"] == lines[heading_start]["page_start"]
        else heading_start
        for heading_start in heading_starts
    ]
    annexes: list[dict] = []

    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        segment = lines[start:end]
        heading_index = heading_starts[position] - start
        heading = segment[heading_index]
        annex_number = ANNEX_RE.fullmatch(heading["text"]).group("number")
        title_line_count = ANNEX_TITLE_LINE_COUNTS.get(annex_number, 0)
        title_start = heading_index + 1
        title = join_text(segment[title_start : title_start + title_line_count]) or None
        page_start, page_end = line_range(segment)
        internal_structures = [
            line["text"]
            for line in segment[title_start:]
            if line["text"].startswith(("Partie ", "Domaine "))
            or re.match(r"\d+(?:\.\d+)+\. ", line["text"])
        ]
        annexes.append(
            {
                "document_id": DOCUMENT_ID,
                "annex": annex_number,
                "heading": heading["text"],
                "title": title,
                "page_start": page_start,
                "page_end": page_end,
                "raw_text": "\n".join(line["text"] for line in segment),
                "eur_lex_markers": markers_in(segment),
                "internal_structures_detected_but_not_parsed": internal_structures,
                "requires_further_processing": True,
                "processing_note": (
                    "Annexe conservée sous forme de texte ligne par ligne; "
                    "la géométrie des tableaux n'est pas reconstruite."
                ),
            }
        )

    return annexes


def build_document(pdf_path: Path = PDF_PATH) -> dict:
    pdf_path = Path(pdf_path).resolve()
    lines, extraction_report = extract_lines(pdf_path)
    first_annex_index = next(
        index for index, line in enumerate(lines) if ANNEX_RE.fullmatch(line["text"])
    )
    main_lines = lines[:first_annex_index]
    annex_lines = lines[first_annex_index:]

    chapter_starts = [
        index for index, line in enumerate(main_lines) if CHAPTER_RE.fullmatch(line["text"])
    ]
    article_starts = [
        index for index, line in enumerate(main_lines) if ARTICLE_RE.fullmatch(line["text"])
    ]
    boundary_starts = sorted(chapter_starts + article_starts + [len(main_lines)])

    chapter_metadata: list[dict] = []
    for position, chapter_start in enumerate(chapter_starts):
        next_chapter = (
            chapter_starts[position + 1]
            if position + 1 < len(chapter_starts)
            else len(main_lines)
        )
        first_article = next(
            index
            for index in article_starts
            if chapter_start < index < next_chapter
        )
        heading = main_lines[chapter_start]
        number = CHAPTER_RE.fullmatch(heading["text"]).group("number")
        title_lines = [
            line
            for line in main_lines[chapter_start + 1 : first_article]
            if not MARKER_RE.fullmatch(line["text"])
        ]
        chapter_segment = main_lines[chapter_start:next_chapter]
        page_start, page_end = line_range(chapter_segment)
        chapter_metadata.append(
            {
                "document_id": DOCUMENT_ID,
                "chapter": number,
                "heading": heading["text"],
                "title": join_text(title_lines),
                "page_start": page_start,
                "page_end": page_end,
                "start_index": chapter_start,
                "end_index": next_chapter,
                "articles": [],
            }
        )

    all_notes: list[dict] = []
    for article_start in article_starts:
        next_boundary = next(index for index in boundary_starts if index > article_start)
        heading = main_lines[article_start]
        chapter = next(
            chapter
            for chapter in reversed(chapter_metadata)
            if chapter["start_index"] < article_start
        )
        article, notes = parse_article(
            heading,
            main_lines[article_start + 1 : next_boundary],
            chapter["chapter"],
            chapter["title"],
        )
        chapter["articles"].append(article)
        all_notes.extend(notes)

    for chapter in chapter_metadata:
        chapter.pop("start_index")
        chapter.pop("end_index")

    first_chapter_index = chapter_starts[0]
    front_matter_lines = main_lines[:first_chapter_index]
    front_page_start, front_page_end = line_range(front_matter_lines)
    annexes = parse_annexes(annex_lines)

    all_markers = markers_in(lines)
    marker_counts = Counter(marker["marker"] for marker in all_markers)
    article_count = sum(len(chapter["articles"]) for chapter in chapter_metadata)
    paragraph_count = sum(
        len(article["paragraphs"])
        for chapter in chapter_metadata
        for article in chapter["articles"]
    )
    detected_titles = [
        line for line in lines if TITLE_RE.fullmatch(line["text"])
    ]
    detected_sections = [
        line for line in lines if SECTION_RE.fullmatch(line["text"])
    ]

    unrecognized_structures = [
        "Aucun en-tête TITRE détecté dans ce règlement.",
        "Aucun en-tête SECTION détecté dans ce règlement.",
        (
            "Les articles 1, 4, 15 et 19 n'ont pas de paragraphes numérotés; "
            "leur corps est conservé dans unnumbered_text."
        ),
        (
            "Les sous-structures Partie, Domaine et les tableaux des annexes "
            "sont signalés mais ne sont pas reconstruits."
        ),
    ]

    return {
        "document_id": DOCUMENT_ID,
        "source_path": str(
            pdf_path.relative_to(PROJECT_ROOT)
            if pdf_path.is_relative_to(PROJECT_ROOT)
            else pdf_path
        ),
        "page_count": extraction_report["page_count"],
        "normalization": {
            "rules": [
                "Suppression des espaces horizontaux superflus.",
                "Recomposition des mots coupés en fin de ligne par U+00AD.",
                "Suppression du seul en-tête/pied de page correspondant au motif exact du document.",
            ],
            **extraction_report,
        },
        "front_matter": {
            "document_id": DOCUMENT_ID,
            "page_start": front_page_start,
            "page_end": front_page_end,
            "text": "\n".join(line["text"] for line in front_matter_lines),
            "eur_lex_markers": markers_in(front_matter_lines),
        },
        "structure": {
            "titles": detected_titles,
            "chapters": chapter_metadata,
            "sections": detected_sections,
            "annexes": annexes,
        },
        "eur_lex_markers": all_markers,
        "notes": all_notes,
        "parsing_report": {
            "chapter_count": len(chapter_metadata),
            "article_count": article_count,
            "numbered_paragraph_count": paragraph_count,
            "annex_count": len(annexes),
            "eur_lex_marker_counts": dict(sorted(marker_counts.items())),
            "unrecognized_or_deferred_structures": unrecognized_structures,
        },
    }


def representative_articles(document: dict, numbers: set[str]) -> list[dict]:
    return [
        article
        for chapter in document["structure"]["chapters"]
        for article in chapter["articles"]
        if article["article"] in numbers
    ]


def main(argv=None) -> None:
    parser, arguments = parse_arguments(
        "Structurer le règlement 2019/2152 en JSON.", PDF_PATH, argv
    )
    try:
        document = build_document(arguments.input)
        write_output(json.dumps(document, ensure_ascii=False, indent=2) + "\n", arguments)
    except (OSError, ValueError, pymupdf.FileDataError) as error:
        parser.error(str(error))
    report = document["parsing_report"]
    print(
        f"Chapitres : {report['chapter_count']} ; articles : {report['article_count']} ; "
        f"paragraphes numérotés : {report['numbered_paragraph_count']} ; "
        f"annexes : {report['annex_count']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
