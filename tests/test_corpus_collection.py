import sys
import unittest
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from corpus_manifest import DOCS
from collect_corpus import resolve, clean_html


class CollectionTests(unittest.TestCase):
    def response(self,content):
        r=requests.Response();r._content=content.encode();r.url='https://www.douane.gouv.fr/fiche/test';return r

    def test_selection_has_45_unique_ascii_paths(self):
        self.assertEqual(len(DOCS),45)
        self.assertEqual(len({r['id'] for r in DOCS}),45)
        for r in DOCS:self.assertTrue(r['nom_fichier'].isascii())

    def test_equivalent_download_links_are_one_resource(self):
        doc=dict(DOCS[20]);doc['selector']='KS-01-26-012'
        r=self.response('<a href="/KS-01-26-012.pdf?version=1.0&download=true">Download</a><a href="/KS-01-26-012.pdf?version=1.0">PDF</a>')
        self.assertIn('KS-01-26-012.pdf',resolve(doc,r))

    def test_ngp_excludes_autosufficient_labels(self):
        doc=dict(DOCS[44])
        r=self.response('<a href="/NGP2026.xls">NGP 2026</a><a href="/NGP2026a.xls">NGP 2026 autosuffisants</a>')
        self.assertEqual(resolve(doc,r),'https://www.douane.gouv.fr/NGP2026.xls')

    def test_access_challenge_is_not_a_document(self):
        r=self.response('<main>Verify you are human '+('x '*500)+'</main>')
        with self.assertRaises(ValueError):clean_html(r,dict(DOCS[1]))

    def test_clean_html_preserves_source_and_text(self):
        r=self.response('<title>Source title</title><nav>Menu</nav><main><h1>EMEBI</h1><p>'+('contenu '*120)+'</p><script>bad()</script></main>')
        result=clean_html(r,dict(DOCS[1])).decode()
        self.assertIn('Consultation:',result)
        self.assertIn(r.url,result)
        self.assertNotIn('<script>',result)


if __name__=='__main__':unittest.main()
