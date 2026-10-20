import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from collect_corpus import redistribution_status


class RedistributionStatusTests(unittest.TestCase):
    def test_explicit_permissions_are_authorized_with_conditions(self):
        for conditions in (
            "CC-BY 4.0 avec exceptions",
            "Licence ouverte Etalab 2.0 sauf mention contraire",
            "Reproduction partielle autorisee avec mention de la source",
            "Reutilisation autorisee avec mention de la source",
        ):
            with self.subTest(conditions=conditions):
                self.assertEqual(
                    redistribution_status(conditions),
                    "autorisee_sous_conditions",
                )

    def test_reserved_un_rights_require_permission(self):
        self.assertEqual(
            redistribution_status("Copyright ONU 2011, tous droits reserves"),
            "non_autorisee_sans_permission",
        )

    def test_missing_or_unknown_conditions_default_to_verification(self):
        for conditions in (None, "", "conditions à vérifier ", "Tous droits réservés"):
            with self.subTest(conditions=conditions):
                self.assertEqual(redistribution_status(conditions), "a_verifier")


if __name__ == "__main__":
    unittest.main()
