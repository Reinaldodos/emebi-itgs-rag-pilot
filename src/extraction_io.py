"""Entrées et sorties communes aux scripts expérimentaux d'extraction."""

import argparse
import os
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_ROOT = PROJECT_ROOT / "corpus"


def parse_arguments(description: str, default_input: Path, argv=None):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--input", type=Path, default=default_input,
        help="PDF source (par défaut : règlement 2019/2152 du corpus local).",
    )
    parser.add_argument(
        "--output", default="-",
        help="Fichier de sortie ; - ou absence d'option : stdout, sans fichier créé.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Autoriser le remplacement d'une sortie existante hors corpus.",
    )
    arguments = parser.parse_args(argv)
    arguments.input = arguments.input.resolve()
    if not arguments.input.is_file():
        parser.error(f"PDF source introuvable : {arguments.input}")
    if arguments.output != "-":
        output = Path(arguments.output).absolute()
        resolved_output = output.resolve()
        if output.is_relative_to(CORPUS_ROOT) or resolved_output.is_relative_to(
            CORPUS_ROOT.resolve()
        ):
            parser.error(
                "Le corpus source est en lecture seule ; choisissez une sortie hors corpus."
            )
        if resolved_output == arguments.input or (
            output.exists() and output.samefile(arguments.input)
        ):
            parser.error("La sortie ne peut pas remplacer le PDF source.")
        if output.is_dir():
            parser.error(f"La sortie est un répertoire : {output}")
        if (output.exists() or output.is_symlink()) and not arguments.force:
            parser.error(f"La sortie existe déjà : {output} (utilisez --force).")
        arguments.output = output
    return parser, arguments


def write_output(content: str, arguments) -> None:
    if arguments.output == "-":
        sys.stdout.write(content)
        return
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    if not arguments.force:
        # Refuse aussi une sortie créée après la validation des arguments.
        with arguments.output.open("x", encoding="utf-8") as output:
            output.write(content)
        return
    # Remplacer le fichier évite de modifier la cible d'un lien symbolique ou
    # physique, qui peut être un autre document du corpus source.
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=arguments.output.parent, delete=False
        ) as output:
            temporary_path = Path(output.name)
            output.write(content)
        os.replace(temporary_path, arguments.output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
