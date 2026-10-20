"""Imports must work without a local corpus or command-line arguments."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parents[1] / "src"

# Dependencies are loaded before installing the guards. Minimal fallbacks let
# these import-only checks run even in a fresh checkout without PDF/HTML tools.
PRELOAD = r'''
import argparse
import contextlib
import importlib.util
import io
import pathlib
import runpy
import subprocess
import sys
import types
from unittest.mock import Mock, patch

for name, attributes in {
    "requests": ("Response", "get"),
    "bs4": ("BeautifulSoup",),
    "pymupdf": ("open",),
}.items():
    try:
        __import__(name)
    except ModuleNotFoundError:
        dependency = types.ModuleType(name)
        for attribute in attributes:
            setattr(dependency, attribute, Mock())
        sys.modules[name] = dependency

source_dir = pathlib.Path(sys.argv[1])
module_path = source_dir / sys.argv[2]
sys.path.insert(0, str(source_dir))
'''

IMPORT_CHECK = PRELOAD + r'''
sys.argv = [str(module_path), "--unexpected-argument"]
sys.dont_write_bytecode = True

def forbidden(*args, **kwargs):
    raise AssertionError("Import attempted an external action")

def audit(event, args):
    if event == "open":
        filename, mode, flags = args
        if isinstance(mode, str) and any(char in mode for char in "wax+"):
            forbidden()
    if event in {
        "os.mkdir", "os.remove", "os.rename", "os.rmdir", "os.system",
        "subprocess.Popen", "socket.connect", "socket.getaddrinfo",
    }:
        forbidden()

sys.addaudithook(audit)
with contextlib.ExitStack() as stack:
    for name in (
        "open", "read_text", "read_bytes", "write_text", "write_bytes",
        "mkdir", "rename", "replace", "unlink", "touch",
    ):
        stack.enter_context(patch.object(pathlib.Path, name, side_effect=forbidden))
    stack.enter_context(patch.object(argparse.ArgumentParser, "parse_args", side_effect=forbidden))
    stack.enter_context(patch.object(sys.modules["requests"], "get", side_effect=forbidden))
    stack.enter_context(patch.object(sys.modules["pymupdf"], "open", side_effect=forbidden))
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    assert stdout.getvalue() == "", stdout.getvalue()
    assert stderr.getvalue() == "", stderr.getvalue()
    if module_path.name in {
        "01_extract.py",
        "02_parse.py",
        "audit_browser_attempts.py",
        "collect_corpus.py",
        "finalize_corpus.py",
        "import_browser_document.py",
    }:
        assert callable(module.main), module_path
'''

HELP_CHECK = PRELOAD + r'''
sys.argv = [str(module_path), "--help"]
try:
    runpy.run_path(str(module_path), run_name="__main__")
except SystemExit as exc:
    assert exc.code == 0, exc.code
else:
    raise AssertionError("The CLI did not handle --help")
'''


class ImportSafetyTests(unittest.TestCase):
    def run_isolated(self, script, filename):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", "-c", script, str(SOURCE_DIR), filename],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(Path(directory).iterdir()), [])
        return result

    def test_all_modules_import_without_external_actions(self):
        for path in sorted(SOURCE_DIR.glob("*.py")):
            with self.subTest(module=path.name):
                result = self.run_isolated(IMPORT_CHECK, path.name)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_importer_cli_still_displays_help(self):
        result = self.run_isolated(HELP_CHECK, "import_browser_document.py")
        self.assertIn("--url", result.stdout)
        self.assertIn("file", result.stdout)


if __name__ == "__main__":
    unittest.main()
