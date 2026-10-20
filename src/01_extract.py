from pathlib import Path

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = (
    PROJECT_ROOT
    / "corpus"
    / "02_union_europeenne"
    / "2019_union_europeenne_reglement_2152_fr.pdf"
)


def main() -> None:
    with pymupdf.open(PDF_PATH) as document:
        print(f"Fichier : {PDF_PATH.name}")
        print(f"Nombre total de pages : {document.page_count}")

        pages_text = [
            (page_number, page.get_text("text"))
            for page_number, page in enumerate(document, start=1)
        ]

    for page_number, text in pages_text:
        print("\n" + "=" * 80)
        print(f"Page {page_number}")
        print("=" * 80)
        print(text[:2000])


if __name__ == "__main__":
    main()
