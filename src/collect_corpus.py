"""Collecte par passes: aucun retry interne, echecs repris a la passe suivante."""
import argparse, csv, hashlib, html, json, re, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup
from corpus_manifest import DOCS, FOLDERS

ROOT = Path(__file__).resolve().parents[1] / 'corpus'
LOCK = threading.Lock()
FIELDS = 'id titre organisme niveau type_document theme date_publication date_version statut_juridique periode_application langue url_source url_telechargement date_consultation nom_fichier format nombre_pages sha256 licence_ou_conditions libre_acces priorite_rag historique_ou_actuel resume observations'.split()
LOGFIELDS = ['horodatage','id','passe','methode','url','url_finale','http','resultat','erreur','octets','duree_secondes']
NOW = datetime.now(timezone.utc).date().isoformat()

def init():
    for folder in FOLDERS + ['metadata','logs','logs/sources','logs/textes','logs/controles']:
        (ROOT/folder).mkdir(parents=True, exist_ok=True)

def save(rows):
    (ROOT/'metadata/etat_collecte.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    successful = [{k:r.get(k,'') for k in FIELDS} for r in rows if r['resultat']=='valide']
    (ROOT/'metadata/catalogue.json').write_text(json.dumps(successful,ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'metadata/catalogue.csv').open('w',encoding='utf-8',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=FIELDS);writer.writeheader();writer.writerows(successful)

def get(url, doc, batch, method):
    started=time.monotonic(); response=None; error=''
    try:
        headers={'User-Agent':'Official-document-corpus-POC/1.0 (public documents; low rate)'}
        if 'publications.europa.eu/resource/' in url:
            headers.update({'Accept':'application/pdf','Accept-Language':'fra','Accept-Max-Cs-Size':'100000000'})
        response=requests.get(url,timeout=(12,35),headers=headers)
        response.raise_for_status()
        if len(response.content)<150: raise ValueError('Reponse trop courte')
        return response
    except Exception as exc:
        error=str(exc); raise
    finally:
        row=dict(horodatage=datetime.now(timezone.utc).isoformat(),id=doc['id'],passe=batch,methode=method,url=url,url_finale=response.url if response is not None else '',http=response.status_code if response is not None else '',resultat='echec' if error else 'recu',erreur=error,octets=len(response.content) if response is not None else 0,duree_secondes=round(time.monotonic()-started,2))
        with LOCK:
            p=ROOT/'logs/telechargements.csv'; exists=p.exists()
            with p.open('a',encoding='utf-8',newline='') as out:
                w=csv.DictWriter(out,fieldnames=LOGFIELDS)
                if not exists:w.writeheader()
                w.writerow(row)

def resolve(doc,response):
    soup=BeautifulSoup(response.content,'html.parser')
    links=[]
    for a in soup.select('a[href]'):
        href=urljoin(response.url,a['href']); label=a.get_text(' ',strip=True)+' '+unquote(href)
        if doc['format']=='pdf' and re.search(r'\.pdf(?:[/?#]|$)',href,re.I):
            selector=doc['selector']
            if selector=='pdf' or selector.lower() in label.lower():links.append(href)
        if doc['format']=='xls' and re.search(r'\.xlsx?(?:[?#]|$)',href,re.I):
            term='ngp' if 'ngp' in doc['selector'] else 'officiel'
            if '2026' in label and term in label.lower() and 'autosuffisant' not in label.lower():links.append(href)
    # The download=true parameter changes the disposition, not the resource/version.
    links=list({re.sub(r'([?&])download=true&?',r'\1',link).rstrip('?&'):link for link in links}.values())
    if len(links)!=1:raise ValueError(f'Lien fichier non univoque ({len(links)}): '+str(links[:8]))
    return links[0]

def clean_html(response,doc):
    soup=BeautifulSoup(response.content,'html.parser')
    text=soup.get_text(' ',strip=True)
    if any(x in text.lower() for x in ['verify you are human','checking your browser','access denied','enable javascript and cookies','captcha']):
        raise ValueError('Controle acces ou page challenge; aucun contournement')
    for e in soup.select('script,style,nav,footer,header,aside,form,noscript,iframe,button'):e.decompose()
    main=soup.select_one('main') or soup.select_one('#content') or soup.select_one('#gauche') or soup.select_one('article') or soup.body or soup
    txt=main.get_text(' ',strip=True)
    if len(txt)<500:raise ValueError('Page HTML sans contenu documentaire suffisant')
    # Metadata are supplementary; dates are not inferred from server timestamps.
    title=BeautifulSoup(response.content,'html.parser').title
    doc['observations']='Copie HTML nettoyee; original HTTP conserve dans logs/sources. Titre source: '+(title.get_text(' ',strip=True) if title else '')
    for a in main.select('[href]'):a['href']=urljoin(response.url,a['href'])
    for a in main.select('[src]'):a['src']=urljoin(response.url,a['src'])
    return ('<!DOCTYPE html><html lang="'+doc['langue']+'"><head><meta charset="utf-8"><title>'+html.escape(doc['titre'])+'</title></head><body><section><h1>'+html.escape(doc['titre'])+'</h1><p>Source: <a href="'+html.escape(response.url)+'">'+html.escape(response.url)+'</a></p><p>Consultation: '+NOW+'</p></section>'+str(main)+'</body></html>').encode('utf-8')

def validate(path,doc):
    data=path.read_bytes();fmt=doc['format']
    if fmt=='pdf':
        if not data.startswith(b'%PDF-'):raise ValueError('Pas un PDF (page erreur possible)')
        info=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,timeout=30,check=True)
        (ROOT/'logs/controles'/f'{doc["id"]}_pdfinfo.txt').write_text(info.stdout,encoding='utf-8')
        doc['nombre_pages']=re.search(r'^Pages:\s+(\d+)',info.stdout,re.M).group(1)
        txt=ROOT/'logs/textes'/f'{doc["id"]}.txt'
        subprocess.run(['pdftotext','-layout',str(path),str(txt)],capture_output=True,timeout=60,check=True)
        if len(txt.read_text(encoding='utf-8').strip())<100 and 'PDF sans texte exploitable' not in doc['observations']:
            doc['observations']+=' PDF sans texte exploitable; OCR requis (outil non disponible).'
    elif fmt=='xsd':
        import xml.etree.ElementTree as ET
        ET.fromstring(data)
    elif fmt=='xls':
        if not(data.startswith(bytes.fromhex('D0CF11E0A1B11AE1')) or data.startswith(b'PK')):raise ValueError('Pas un fichier Excel')
        controls=[ROOT/'logs/controles'/(path.stem+'.csv'),ROOT/'logs/controles'/(path.name+'.csv')]
        prior=next((p for p in controls if p.exists()),None)
        if prior and doc.get('sha256')==hashlib.sha256(data).hexdigest():
            with prior.open(encoding='utf-8',newline='') as f:
                if len(list(csv.reader(f)))<2:raise ValueError('Export de controle XLS vide')
            return
        # Reopen without changing the original with LibreOffice in an isolated profile.
        result=subprocess.run(['libreoffice','-env:UserInstallation=file:///tmp/corpus_lo_'+doc['id'],'--headless','--convert-to','csv','--outdir',str(ROOT/'logs/controles'),str(path)],capture_output=True,text=True,timeout=45)
        if result.returncode or not (ROOT/'logs/controles'/(path.stem+'.csv')).exists():raise ValueError('Excel ouverture non validee: '+result.stderr)
    elif fmt=='html':
        soup=BeautifulSoup(data,'html.parser')
        if not soup.h1 or len(soup.get_text())<500:raise ValueError('HTML non exploitable')
    doc['sha256']=hashlib.sha256(data).hexdigest()

def collect(doc,batch):
    doc=dict(doc)
    try:
        url=doc['url_telechargement'] or doc['url_source']
        if batch==7:
            identifiers={'D17':('consolidation','02021R1704-20260510'),'D38':('consolidation','02009R0471-20161223'),'D18':('oj','L_202600047')}
            if doc['id'] not in identifiers:raise ValueError('Replis officiels disponibles epuises; import manuel requis')
            system,identifier=identifiers[doc['id']]
            url='https://publications.europa.eu/resource/'+system+'/'+identifier
            doc['format']='pdf';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.pdf'))
        if batch==6:
            publications={'D16':'https://op.europa.eu/it/publication-detail/-/publication/71985d1b-174c-11f1-8870-01aa75ed71a1/language-en','D41':'https://op.europa.eu/lt/publication-detail/-/publication/594755e8-0d1a-11eb-bc07-01aa75ed71a1/language-fr'}
            if doc['id'] not in publications:raise ValueError('Aucun autre point de telechargement officiel verifie; originaux manquants consignés')
            response=get(publications[doc['id']],doc,batch,'page_office_publications')
            (ROOT/'logs/sources'/f'{doc["id"]}_office_publications.html').write_bytes(response.content)
            soup=BeautifulSoup(response.content,'html.parser')
            a=soup.select_one('a[data-language="fr"][data-format="pdfa2a"][data-uri]')
            if not a:raise ValueError('PDF francais non expose par Office des publications')
            url=urljoin(response.url,a['data-uri'])
            doc['format']='pdf';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.pdf'))
        if batch==5:
            celex={'D16':'02020R1197-20260305','D17':'02021R1704-20260510','D18':'32026R0047','D37':'32004R0638','D38':'02009R0471-20161223','D39':'32025R1926','D41':'32020R1470'}
            if doc['id'] not in celex:raise ValueError('Pas de nouveau service officiel libre disponible pour ce texte francais; original a importer manuellement')
            url='https://publications.europa.eu/resource/celex/'+celex[doc['id']]
            doc['format']='pdf';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.pdf'))
            doc['observations']='Original Office des publications via interface REST Cellar documentee; source https://op.europa.eu/en/web/cellar/cellar-data/publications. '
        if batch==4:
            alternatives={
                'D12':'https://www.legifrance.gouv.fr/download/pdf?id=0HBNfiPl0shPIt5EdufogPJM530GUFJ9awgXQ4O_4Uw=',
                'D34':'https://www.legifrance.gouv.fr/download/pdf?id=QsPi44J2BiKdxWSq9iK5I2KprXcSf2MrYdYfS2fg9qk=',
                'D18':'https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=OJ:L_202600047',
                'D19':'https://www.iweps.be/wp-content/uploads/2025/08/REGLEMENT-CE_223-2009-du-11.03.2009_FR.pdf',
                'D16':'https://op.europa.eu/it/publication-detail/-/publication/71985d1b-174c-11f1-8870-01aa75ed71a1/language-en',
            }
            if doc['id'] not in alternatives:raise ValueError('Pas de nouveau lien original officiel verifie; echec conserve, reprise manuelle requise')
            url=alternatives[doc['id']]
            if doc['id']!='D16':
                doc['format']='pdf';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.pdf'))
        if batch>=2 and doc['id'] in ('D40','D45'):
            url='https://www.douane.gouv.fr/fiche/comment-remplir-sa-reponse-lenquete-mensuelle-statistique-sur-les-echanges-de-biens-intra-ue'
        if batch in (2,3) and 'legifrance.gouv.fr' in url:
            raise ValueError('HTTP 403 premiere passe; repli navigateur necessaire, pas de repetition automatique ni contournement')
        if batch==2 and 'eur-lex.europa.eu' in url:
            url=url.replace('/TXT/PDF/','/TXT/HTML/');doc['format']='html';doc['nom_fichier']=str(Path(doc['nom_fichier']).with_suffix('.html'))
            doc['observations']='Repli HTML EUR-Lex apres echec PDF. '
        response=get(url,doc,batch,'direct' if batch==1 else 'repli_html_ou_resolution')
        if batch==4 and doc['id']=='D16':
            (ROOT/'logs/sources'/f'{doc["id"]}_office_publications.html').write_bytes(response.content)
            raise ValueError('Page Office des publications sauvegardee pour resolution; ce n est pas le document original')
        if doc['format'] in ('pdf','xls') and not doc['url_telechargement']:
            (ROOT/'logs/sources'/f'{doc["id"]}.html').write_bytes(response.content)
            url=resolve(doc,response);response=get(url,doc,batch,'piece_jointe_source')
        if doc['format']=='html':
            (ROOT/'logs/sources'/f'{doc["id"]}.html').write_bytes(response.content)
            data=clean_html(response,doc)
        else:data=response.content
        path=ROOT/doc['nom_fichier'];temp=path.with_suffix(path.suffix+'.part');temp.write_bytes(data)
        validate(temp,doc)
        temp.replace(path)
        doc.update(resultat='valide',date_consultation=NOW,url_telechargement=response.url,libre_acces='oui')
        doc.pop('erreur',None)
    except Exception as exc:
        doc.update(resultat='echec',erreur=str(exc))
    return doc

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pass-number',type=int,default=1);parser.add_argument('--only');args=parser.parse_args();init()
    state=ROOT/'metadata/etat_collecte.json'
    rows=json.loads(state.read_text()) if state.exists() else DOCS
    pending=[r for r in rows if r['resultat']!='valide' and (not args.only or r['id'] in args.only.split(','))]
    print(f'PASSE {args.pass_number}: {len(pending)} documents a tenter',flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(collect,r,args.pass_number):r['id'] for r in pending}
        for n,future in enumerate(as_completed(jobs),1):
            r=future.result();rows=[r if old['id']==r['id'] else old for old in rows];save(rows)
            ok=sum(x['resultat']=='valide' for x in rows)
            print(f'{n}/{len(pending)} {r["id"]} {r["resultat"]} | valides={ok}/45 restants={45-ok}'+(' | '+r.get('erreur','')[:220] if r['resultat']=='echec' else ''),flush=True)
    print('FIN PASSE',args.pass_number,flush=True)

if __name__=='__main__':main()
