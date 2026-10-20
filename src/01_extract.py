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


def extract_text(pdf_path: Path) -> str:
    with pymupdf.open(pdf_path) as document:
        sections = [
            f"Fichier : {pdf_path.name}",
            f"Nombre total de pages : {document.page_count}",
        ]

        pages_text = [
            (page_number, page.get_text("text"))
            for page_number, page in enumerate(document, start=1)
        ]

    for page_number, text in pages_text:
        sections.extend(
            ["\n" + "=" * 80, f"Page {page_number}", "=" * 80, text[:2000]]
        )
    return "\n".join(sections) + "\n"


def main(argv=None) -> None:
    parser, arguments = parse_arguments(
        "Afficher un aperçu textuel d'un PDF.", PDF_PATH, argv
    )
    try:
        write_output(extract_text(arguments.input), arguments)
    except (OSError, ValueError, pymupdf.FileDataError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
