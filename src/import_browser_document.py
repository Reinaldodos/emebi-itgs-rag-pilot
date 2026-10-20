"""Importer un telechargement obtenu par l'interface ordinaire du navigateur."""
import argparse,json,time
from pathlib import Path
import requests
from collect_corpus import ROOT,init,clean_html,validate,save,NOW,LOCK,LOGFIELDS
import csv

p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('file');p.add_argument('--url',required=True);args=p.parse_args()
init();rows=json.loads((ROOT/'metadata/etat_collecte.json').read_text());doc=next(r for r in rows if r['id']==args.id)
raw=Path(args.file).read_bytes()
if raw.startswith(b'%PDF-'):
    doc['format']='pdf';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.pdf'));data=raw
else:
    doc['format']='html';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.html'))
    response=requests.Response();response._content=raw;response.url=args.url
    (ROOT/'logs/sources'/f'{doc["id"]}.html').write_bytes(raw);data=clean_html(response,doc)
path=ROOT/doc['nom_fichier'];path.write_bytes(data);validate(path,doc)
doc.update(resultat='valide',date_consultation=NOW,url_telechargement=args.url,libre_acces='oui')
doc.pop('erreur',None);save(rows)
with (ROOT/'logs/telechargements.csv').open('a',encoding='utf-8',newline='') as out:
    csv.DictWriter(out,fieldnames=LOGFIELDS).writerow(dict(horodatage=NOW,id=args.id,passe=3,methode='navigateur_ordinaire_import',url=args.url,url_finale=args.url,http='',resultat='valide',erreur='',octets=len(raw),duree_secondes=''))
ok=sum(r['resultat']=='valide' for r in rows);print(f'{args.id} valide; {ok}/45 telecharges; {45-ok} restants')
