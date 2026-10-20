import importlib.util
import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "src" / "02_parse.py"
SPEC = importlib.util.spec_from_file_location("parse_regulation", MODULE_PATH)
parse_regulation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parse_regulation)


class ParseRegulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = parse_regulation.build_document()
        cls.chapters = cls.document["structure"]["chapters"]
        cls.articles = [
            article for chapter in cls.chapters for article in chapter["articles"]
        ]

    def test_expected_structure_is_detected(self):
        report = self.document["parsing_report"]
        self.assertEqual(report["chapter_count"], 9)
        self.assertEqual(report["article_count"], 26)
        self.assertEqual(report["numbered_paragraph_count"], 99)
        self.assertEqual(report["annex_count"], 6)
        self.assertEqual(
            [article["article"] for article in self.articles],
            [str(number) for number in range(1, 27)],
        )
        self.assertEqual(
            {
                article["article"]
                for article in self.articles
                if article["unnumbered_text"] is not None
            },
            {"1", "4", "15", "19"},
        )

    def test_normalization_and_markers_are_auditable(self):
        normalization = self.document["normalization"]
        self.assertEqual(
            len(normalization["removed_repetitive_headers_and_footers"]), 36
        )
        self.assertNotIn("\u00ad", json.dumps(self.document, ensure_ascii=False))
        self.assertEqual(
            self.document["parsing_report"]["eur_lex_marker_counts"],
            {"►B": 1, "►M1": 1, "►M2": 1, "▼B": 33, "▼M2": 2},
        )

    def test_structured_units_keep_provenance(self):
        for chapter in self.chapters:
            self.assertEqual(chapter["document_id"], parse_regulation.DOCUMENT_ID)
            self.assertLessEqual(chapter["page_start"], chapter["page_end"])
            for article in chapter["articles"]:
                self.assertEqual(article["document_id"], parse_regulation.DOCUMENT_ID)
                self.assertLessEqual(article["page_start"], article["page_end"])
                for paragraph in article["paragraphs"]:
                    self.assertEqual(
                        paragraph["document_id"], parse_regulation.DOCUMENT_ID
                    )
                    self.assertEqual(paragraph["article"], article["article"])
                    self.assertLessEqual(
                        paragraph["page_start"], paragraph["page_end"]
                    )

        for annex in self.document["structure"]["annexes"]:
            self.assertEqual(annex["document_id"], parse_regulation.DOCUMENT_ID)
            self.assertTrue(annex["requires_further_processing"])
            self.assertLessEqual(annex["page_start"], annex["page_end"])

        annexes = self.document["structure"]["annexes"]
        self.assertEqual((annexes[0]["page_start"], annexes[0]["page_end"]), (22, 24))
        self.assertIn(
            {"marker": "▼B", "page": 25}, annexes[1]["eur_lex_markers"]
        )


if __name__ == "__main__":
    unittest.main()
