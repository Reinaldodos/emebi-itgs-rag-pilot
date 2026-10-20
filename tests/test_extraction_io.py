import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ("01_extract.py", "02_parse.py")


class ExtractionCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="extraction cli ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pdf = self.root / "source document.pdf"
        # Fixture générée à l'exécution : aucun document tiers ni binaire commis.
        with pymupdf.open() as document:
            page = document.new_page()
            page.insert_text(
                (72, 72),
                "Introduction\nCHAPITRE I\nObjet\nArticle premier\nChamp\n"
                "1.\nTexte du paragraphe.\nANNEXE I\nAnnexe de test\nContenu",
            )
            document.save(self.pdf)
        self.original_hash = hashlib.sha256(self.pdf.read_bytes()).hexdigest()

    def tearDown(self):
        self.assertEqual(
            hashlib.sha256(self.pdf.read_bytes()).hexdigest(), self.original_hash
        )

    def run_cli(self, script, *arguments, source=None):
        return subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "src" / script),
             "--input", str(source or self.pdf), *map(str, arguments)],
            cwd=self.root, capture_output=True, text=True, check=False, timeout=15,
        )

    def assert_content(self, script, content):
        if script == "02_parse.py":
            document = json.loads(content)
            self.assertEqual(document["source_path"], str(self.pdf))
            self.assertEqual(document["parsing_report"]["article_count"], 1)
        else:
            self.assertIn("Fichier : source document.pdf", content)
            self.assertIn("Texte du paragraphe.", content)

    def test_default_and_explicit_stdout_create_no_files(self):
        original_files = set(self.root.iterdir())
        for script in SCRIPTS:
            for arguments in ((), ("--output", "-")):
                with self.subTest(script=script, arguments=arguments):
                    result = self.run_cli(script, *arguments)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assert_content(script, result.stdout)
                    self.assertEqual(set(self.root.iterdir()), original_files)

    def test_explicit_output_creates_parent_directories(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = self.root / "results" / f"{script}.result"
                result = self.run_cli(script, "--output", output)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assert_content(script, output.read_text(encoding="utf-8"))

    def test_relative_paths_are_resolved_from_working_directory(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = Path("relative-results") / f"{script}.result"
                result = self.run_cli(
                    script, "--output", output, source=Path(self.pdf.name)
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_content(
                    script, (self.root / output).read_text(encoding="utf-8")
                )

    def test_overwrite_requires_force(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = self.root / f"{script}.result"
                output.write_text("existing result", encoding="utf-8")
                result = self.run_cli(script, "--output", output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("--force", result.stderr)
                self.assertEqual(output.read_text(), "existing result")
                result = self.run_cli(script, "--output", output, "--force")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_content(script, output.read_text(encoding="utf-8"))

    def test_input_cannot_be_overwritten_even_with_force_or_an_alias(self):
        alias = self.root / "source-alias.pdf"
        alias.hardlink_to(self.pdf)
        for script in SCRIPTS:
            for output in (self.pdf, alias):
                with self.subTest(script=script, output=output):
                    result = self.run_cli(script, "--output", output, "--force")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("PDF source", result.stderr)

    def test_corpus_output_is_refused_even_with_force_and_symlink(self):
        corpus = PROJECT_ROOT / "corpus"
        alias = self.root / "corpus-alias"
        alias.symlink_to(corpus, target_is_directory=True)
        for script in SCRIPTS:
            for directory in (corpus, alias):
                with self.subTest(script=script, directory=directory):
                    output = directory / "cli-test-output-that-must-not-exist.json"
                    self.assertFalse(output.exists())
                    result = self.run_cli(script, "--output", output, "--force")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("lecture seule", result.stderr)
                    self.assertFalse(output.exists())

    def test_forced_replacement_does_not_change_an_unrelated_hardlink(self):
        other_source = self.root / "other-source.pdf"
        other_source.write_bytes(self.pdf.read_bytes())
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = self.root / f"{script}.linked-result"
                output.hardlink_to(other_source)
                result = self.run_cli(script, "--output", output, "--force")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(other_source.read_bytes(), self.pdf.read_bytes())
                self.assert_content(script, output.read_text(encoding="utf-8"))

    def test_missing_input_fails_without_creating_output(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = self.root / "new-directory" / "result"
                result = self.run_cli(
                    script, "--output", output, source=self.root / "missing.pdf"
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("introuvable", result.stderr)
                self.assertFalse(output.parent.exists())

    def test_invalid_pdf_fails_without_creating_output(self):
        invalid_pdf = self.root / "invalid.pdf"
        invalid_pdf.write_text("not a PDF", encoding="utf-8")
        for script in SCRIPTS:
            with self.subTest(script=script):
                output = self.root / "new-directory" / "result"
                result = self.run_cli(script, "--output", output, source=invalid_pdf)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.parent.exists())


if __name__ == "__main__":
    unittest.main()
