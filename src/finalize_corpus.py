"""Verifier, documenter les incertitudes et produire les catalogues concordants."""
import csv,json,hashlib,re
from collections import Counter,defaultdict
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from collect_corpus import ROOT,NOW,save,validate,clean_html,FOLDERS

rows=json.loads((ROOT/'metadata/etat_collecte.json').read_text())
byid={r['id']:r for r in rows}
updates={
 'D01':dict(date_publication='',date_version='2025-12-19',statut_juridique='Notice administrative EMEBI 2026; ne remplace pas les textes normatifs'),
 'D02':dict(date_version='2025-12-30'),
 'D04':dict(date_version='2026-04-16'),
 'D05':dict(date_version='2026-01-05',periode_application='Calendriers 2023 a 2026; choisir le mois et le millesime de reference'),
 'D06':dict(date_publication='',date_version='2022-01-31; v1.0'),
 'D07':dict(date_publication='',date_version='2022-02-24; v1.3.9',statut_juridique='Guide technique provisoire publie par DGDDI; maintien operationnel a confirmer'),
 'D09':dict(date_publication='',date_version='2022-03-07; v5.1.7'),
 'D11':dict(date_version='2019-03-25',statut_juridique='Loi consolidee affichee en vigueur au 2026-10-06; article 5 abroge explicitement conserve'),
 'D12':dict(date_publication='2025-11-25',date_version='2025-10-27',url_source='https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000052835952',statut_juridique='Programme des enquetes 2026; EMEBI dans annexe obligatoire lue au navigateur, original non obtenu'),
 'D13':dict(organisme='Comite du label (INSEE)',date_publication='',date_version='2024-10-18',periode_application='2025-2029',statut_juridique='Avis du Comite du label: interet general, qualite statistique et caractere obligatoire 2025-2029'),
 'D14':dict(titre='Courrier des statistiques numero 12: Les statistiques du commerce exterieur - Specificites, defis et dimension europeenne',date_publication='2024-12',date_version='Numero 12, decembre 2024',licence_ou_conditions='Reproduction partielle autorisee avec mention de la source et de l auteur (colophon p. 2); droits photos a verifier'),
 'D15':dict(statut_juridique='Reglement en vigueur; consolidation documentaire sans effet juridique autonome, version 2026-05-10',periode_application='Cadre general depuis 2021; dispositions ITGS intra-UE et fiscales/douanieres visees art.26 depuis 2022',date_publication='2019-12-17',date_version='2026-05-10'),
 'D16':dict(date_publication='2020-08-18',date_version='2026-03-05',statut_juridique='Reglement execution 2020/1197, consolidation 2026-03-05; outil documentaire sans effet juridique autonome; originaux JO font foi',priorite_rag='essentielle'),
 'D19':dict(date_publication='2009-03-31',date_version='2024-12-26',statut_juridique='Reglement 223/2009; consolidation documentaire 2024-12-26 controlee visuellement; sans effet juridique autonome',priorite_rag='utile'),
 'D17':dict(date_version='2026-05-10',url_source='https://eur-lex.europa.eu/eli/reg_del/2021/1704/2026-05-10/fra',statut_juridique='Consolidation 2026-05-10 prioritaire; original 2021 modifie par 2026/47; fichier non obtenu'),
 'D18':dict(date_publication='2026-04-20',date_version='2025-12-10',statut_juridique='Acte modificatif; entree en vigueur 2026-05-10, dates de dispositions a confirmer sur original'),
 'D20':dict(date_publication='2018',date_version='2017-11-16',statut_juridique='Instrument d autoregulation du Systeme statistique europeen, non reglement',licence_ou_conditions='Reutilisation autorisee avec mention de la source; decision 2011/833/UE; exceptions droits tiers (p. 2)'),
 'D21':dict(titre='User manual on international trade in goods statistics - 2026 edition',date_version='2026 edition; manuscrit 2026-02'),
 'D22':dict(date_version='2026 edition; manuscrit 2026-01'),
 'D23':dict(date_version='2026 edition; manuscrit 2026-01'),
 'D24':dict(date_version='2025 edition; manuscrit 2025-12'),
 'D25':dict(date_version='2026 edition; manuscrit 2026-01'),
 'D27':dict(date_version='2026-02-02 White Cover',statut_juridique='Recommandations IMTS adoptees Commission statistique decision 57/108 (mars 2026); fichier White Cover soumis a revision editoriale; non contraignant'),
 'D28':dict(date_publication='2026-03-25',date_version='Rapport 57e session, 3-6 mars 2026'),
 'D29':dict(date_version='Edition 2010, Series M 52 Rev.3',licence_ou_conditions='Copyright ONU 2011, tous droits reserves; reutilisation/indexation et diffusion a verifier'),
 'D30':dict(date_version='Revision 1, edition 2013, Series F 87 Rev.1',licence_ou_conditions='Copyright ONU 2013, tous droits reserves; reutilisation/indexation et diffusion a verifier'),
 'D31':dict(date_publication='2008',date_version='Supplement 2008, Series F 87 Add.1',licence_ou_conditions='Copyright ONU 2008, tous droits reserves; reutilisation/indexation et diffusion a verifier'),
 'D32':dict(date_version='2025-01-30 White Cover'),
 'D33':dict(date_publication='2022-02-08',date_version='',statut_juridique='Information administrative historique sur la transition 2022, non texte normatif'),
 'D34':dict(date_publication='',date_version='2022-02-04',statut_juridique='Decret original de transition; dispositions applicables aux operations depuis 2022-01-01; evolutions ulterieures a verifier'),
 'D35':dict(date_version='2025-01-01 affichee; consultation 2026-10-06',historique_ou_actuel='historique',statut_juridique='Abrogation annoncee par ordonnance 2025-1247; effet au 2026-09-01 indique dans nota, avec exceptions. NON valide comme base applicable au 2026-10-06'),
 'D36':dict(statut_juridique='Applicabilite article par article non validee; original non obtenu'),
 'D37':dict(date_publication='2004-04-07',date_version='Texte initial 2004-03-31',statut_juridique='Abroge avec effet au 2022-01-01 (art.25 reglement 2019/2152); texte initial historique non consolide',periode_application='Ancien cadre intra-UE, avant 2022; texte initial sans modifications ulterieures'),
 'D39':dict(date_publication='2025-10-31',date_version='2025-09-22',periode_application='2026'),
 'D40':dict(date_version='Millesime 2026',statut_juridique='Referentiel NC8 libelles officiels; force normative dans reglement 2025/1926'),
 'D41':dict(date_publication='2020-10-13',date_version='2020-10-12',periode_application='Depuis 2021-01-01',statut_juridique='Reglement de geonomenclature; entree en vigueur 2021-01-01 (art.5); reference reprise dans manuel Eurostat 2026'),
 'D42':dict(date_version='2026 edition; manuscrit 2026-03'),
 'D45':dict(date_version='Millesime 2026',statut_juridique='Referentiel DGDDI NGP, distinct de NC8; champ d usage a confirmer'),
}
for key,values in updates.items():byid[key].update(values)
for key in ['D08','D10','D31','D32']:byid[key]['priorite_rag']='complémentaire'
for r in rows:
    if r['licence_ou_conditions']=='conditions a verifier':r['licence_ou_conditions']='conditions à vérifier'
notes={
 'D02':'La page regroupe aussi NC8/NGP 2022-2025: segmenter chaque millesime avant indexation. Les XLS retenus sont ceux de 2026.',
 'D04':'FAQ textuelle archivee; videos liees non telechargees et non transcrites.',
 'D05':'Plusieurs calendriers historiques sur une meme page; ne pas confondre echeance du depot et mois de reference.',
 'D06':'Fichier remis en ligne sous repertoire 2025-08 mais contenu date 31/01/2022. Millesime et version verifies sur couverture.',
 'D07':'Nom URL v1.3.8 mais couverture v1.3.9 du 24/02/2022: version du contenu retenue.',
 'D08':'XSD syntaxiquement XML valide; validation de fichiers declaratifs contre ce schema non testee.',
 'D09':'Nom URL v5.1.6 mais couverture v5.1.7 du 07/03/2022: version du contenu retenue.',
 'D11':'Autorite: legislateur francais; diffusion SGG/DILA Legifrance. Copie navigateur du texte consolide incluant articles abroges clairement etiquetes.',
 'D13':'Autorite emettrice: Comite du label de la statistique publique (INSEE); diffusion sur CNIS. Montant 460000 euros decrit la population de cet avis: ne pas en deduire un seuil universel de declaration EMEBI.',
 'D14':'Original complet du numero (160 pages), article commerce exterieur commence p. 7 imprimee. Autres articles hors perimetre: filtrer lors du decoupage RAG.',
 'D19':'Copie officielle de diffusion IWEPS du texte EUR-Lex, 26 pages images; identifiant/version verifies visuellement sur p.1. PDF conservé, OCR non produit faute de moteur installe; ne pas indexer sans OCR.',
 'D24':'Edition 2025 publiee en 2026, non doublon d un manuel 2026.',
 'D25':'Coquille couverture invoicing country; titre interieur invoicing currency retenu.',
 'D27':'Adoption confirmee par D28 decision 57/108; le fichier acquis reste White Cover et ne doit pas etre presente comme edition editoriale definitive.',
 'D29':'Ancien cadre conceptuel conserve pour interpretation des manuels et comparaisons avec IMTS 2026.',
 'D30':'Manuel fonde sur IMTS 2010; ne pas assimiler sa date de fichier PDF a la date de publication.',
 'D32':'Contient egalement statistiques de services: conserver seulement chapitres utiles a integration entreprises/commerce de biens.',
 'D35':'Le navigateur affiche simultanement VERSION EN VIGUEUR et Abroge par ordonnance. Validation juridique des exceptions et de la recodification indispensable; fichier non collecte.',
 'D43':'Date de publication/mise a jour non indiquee: laisser vide, ne pas inferer du millesime de collecte.',
 'D44':'Texte comporte des estimations historiques de janvier 2022; ne pas les presenter comme mesure de qualite 2026. Date de publication/mise a jour non determinee.',
}
for key,note in notes.items():
    if note not in byid[key].get('observations',''):byid[key]['observations']=(byid[key].get('observations','')+' '+note).strip()

# Rename only artifacts whose verified content year differs from preliminary selection.
for key,year in [('D06','2022'),('D33','2022')]:
    r=byid[key];old=ROOT/r['nom_fichier'];new=old.with_name(re.sub(r'^\d{4}',year,old.name))
    if old!=new and old.exists():old.rename(new)
    r['nom_fichier']=str(new.relative_to(ROOT))

for r in rows:
    if r['resultat']!='valide':continue
    source=ROOT/'logs/sources'/f'{r["id"]}.html'
    if source.exists():
        soup=BeautifulSoup(source.read_bytes(),'html.parser')
        meta=soup.select_one('meta[property="og:book:release_date"]')
        if meta:r['date_publication']=meta['content'].split('T')[0]
    if r['organisme']=='Eurostat' and r['format']=='pdf' and r['id']!='D20':
        text=(ROOT/'logs/textes'/f'{r["id"]}.txt').read_text()
        if 'CC-BY 4.0' in text:r['licence_ou_conditions']='CC-BY 4.0 sauf elements tiers (notamment photos de couverture); mention explicite dans colophon'
    if r['id']=='D11':r['licence_ou_conditions']='Licence ouverte Etalab 2.0 sauf mention contraire; mention explicite pied de page Legifrance'
    if r['format']=='html' and source.exists():
        response=requests.Response();response._content=source.read_bytes();response.url=r['url_telechargement']
        previous=r['observations'];(ROOT/r['nom_fichier']).write_bytes(clean_html(response,r));r['observations']=previous
    if r['historique_ou_actuel']=='actuel' and r['type_document']=='manuel methodologique':
        r['statut_juridique']='Manuel methodologique non contraignant; edition conservee, distincte du droit applicable'
    for key,notice in [('date_publication',' Date de publication non determinee (champ vide).'),('date_version',' Date/version documentaire non determinee (champ vide).'),('periode_application',' Periode d application non explicitee ou non applicable a une documentation non normative.')]:
        if not r[key] and notice not in r['observations']:r['observations']+=notice
    r['resume']='Document officiel sur '+r['theme'].lower()+'. '+('Usage historique, ne constitue pas une obligation actuelle.' if r['historique_ou_actuel']=='historique' else 'A utiliser avec le champ geographique et la version indiques.')
    validate(ROOT/r['nom_fichier'],r)
save(rows)

excluded=[
 ('X01','NC8 2026 libelles autosuffisants','https://www.douane.gouv.fr/sites/default/files/2025-12/08/NC2026_annexe7.xls','Libelles simplifies; preferer libelles officiels NC8 D40, pas un texte normatif'),
 ('X02','NGP 2026 libelles autosuffisants','https://www.douane.gouv.fr/sites/default/files/2025-12/15/Ngp%2Bcana2026a%20annexe4.xls','Preferer referentiel NGP retenu D45; eviter quasi doublon'),
 ('X03','NC8 2025 libelles officiels','https://www.douane.gouv.fr/sites/default/files/2024-12/17/NC2025_annexe6.xls','Millesime remplace par 2026 pour ce POC; lien seulement examine dans D02'),
 ('X04','NGP 2025','https://www.douane.gouv.fr/sites/default/files/2024-12/06/Ngp%2Bcana2025%20annexe3_vd.xls','Millesime anterieur non necessaire a transition de 2022; lien examine dans D02'),
 ('X05','Questions frequentes DEBWEB 2020','https://www.douane.gouv.fr/sites/default/files/uploads/files/2020-07/Questions%20fr%C3%A9quentes%20DebWeb%202020.pdf','FAQ ancienne DEB, preferee FAQ EMEBI/TVA D04; lien examine dans D33'),
 ('X06','Reglementation sur la reponse EMEBI','https://www.douane.gouv.fr/fiche/reglementation-sur-la-reponse-lenquete-mensuelle-statistique-sur-les-echanges-de-biens-intra','Page de presentation redondante avec notice et textes; non telechargee, examinee pendant inventaire'),
]
with (ROOT/'metadata/documents_non_retenus.csv').open('w',encoding='utf-8',newline='') as out:
    w=csv.writer(out);w.writerow(['id','titre','url_source','date_consultation','raison_exclusion']);w.writerows([(i,t,u,NOW,reason) for i,t,u,reason in excluded])
failed=[r for r in rows if r['resultat']!='valide']
with (ROOT/'metadata/documents_en_echec.csv').open('w',encoding='utf-8',newline='') as out:
    w=csv.DictWriter(out,fieldnames=['id','titre','url_source','erreur','action_recommandee']);w.writeheader()
    for r in failed:w.writerow({k:r.get(k,'') for k in ['id','titre','url_source','erreur']}|{'action_recommandee':'Telecharger l original depuis le navigateur habituel puis importer avec src/import_browser_document.py; verifier statut et millesime'})

ok=[r for r in rows if r['resultat']=='valide'];hashes=defaultdict(list)
for r in ok:hashes[r['sha256']].append(r['id'])
duplicates={k:v for k,v in hashes.items() if len(v)>1}
files={str(p.relative_to(ROOT)) for f in FOLDERS if (ROOT/f).exists() for p in (ROOT/f).iterdir() if p.is_file() and not p.name.endswith('.part')}
expected={r['nom_fichier'] for r in ok}
assert files==expected,(files-expected,expected-files)
with (ROOT/'metadata/catalogue.csv').open(encoding='utf-8',newline='') as f:assert list(csv.DictReader(f))==json.loads((ROOT/'metadata/catalogue.json').read_text())
assert all(hashlib.sha256((ROOT/r['nom_fichier']).read_bytes()).hexdigest()==r['sha256'] for r in ok)
summary={'date_controle':NOW,'candidats_selectionnes':45,'documents_examines_inventaire':45+len(excluded),'documents_telecharges_valides':len(ok),'documents_ecartes':len(excluded),'documents_en_echec':len(failed),'doublons_sha256':duplicates,'concordance_catalogue_fichiers':True,'concordance_csv_json':True,'repartition':{field:dict(Counter(r[field] for r in ok)) for field in ['niveau','organisme','type_document','langue','format']},'volume_octets':sum((ROOT/r['nom_fichier']).stat().st_size for r in ok)}
(ROOT/'logs/controle_final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
top=['D01','D03','D04','D05','D11','D13','D15','D16','D22','D27']
report=['# Bilan du corpus', '', f'Controle du {NOW}. Livraison partielle: {len(ok)} documents valides sur 45 selectionnes; {len(failed)} originaux restent a obtenir.', '',f'Inventaire: {45+len(excluded)} documents examines, dont 45 candidats retenus et {len(excluded)} exclus. Les aliases de liens ne sont pas comptes comme documents.', '', '## Repartition des documents valides', '']
for field in ['niveau','organisme','type_document','langue','format']:
    report.append('- '+field+': '+', '.join(f'{k}: {v}' for k,v in summary['repartition'][field].items()))
report+=['','## Dix documents prioritaires disponibles','']
for i,key in enumerate(top,1):
    r=byid[key];report.append(f'{i}. {key} — [{r["titre"]}](../{r["nom_fichier"]}) : {r["theme"]}.')
report+=['','## Originaux manquants','']+[f'- {r["id"]} — {r["titre"]}: {r.get("erreur","")}' for r in failed]
report+=['','## Lacunes et validations requises','',
 '- Priorite de complement: arrete 2026, reglement 2021/1704 consolide, acte modificatif 2026/47 et nomenclature combinee normative 2026. Le reglement 2020/1197 consolide et la geonomenclature normative ont ete recuperes. Les manuels ne remplacent pas les textes manquants.',
 '- Reconstituer la base fiscale TVA apres recodification 2026. Article 289 B: affichage de version en vigueur et nota d abrogation au 1er septembre 2026 avec exceptions; ne pas l utiliser comme base actuelle sans avis juridique.',
 '- Confirmer avec DGDDI le plan annuel de selection EMEBI et la portee des chiffres descriptifs CNIS; obligation liee a la selection/notification, pas a un seuil universel deduit d un avis.',
 '- Confirmer le maintien des guides techniques 2022 toujours lies sur la page courante. Les versions du contenu different parfois du nom du fichier.',
 '- IMTS 2026: recommandations adoptees (D28, decision 57/108), mais original acquis White Cover soumis a revision editoriale; confirmer calendrier national de mise en oeuvre.',
 '- Verifier droits de reutilisation pour indexation, redistribution et publication RAG, surtout documents ONU tous droits reserves et photos tiers. Acces public ne signifie pas licence ouverte.',
 '- Videos Douane non transcrites, tables de passage annuelles NC8 non retenues, liste de l echantillon individuel non publique. Ces lacunes ne sont pas masquees par des donnees fabriquees.',
 '- Controle technique de tous les fichiers (PDF pdfinfo et extraction integrale pdftotext; HTML parse; XSD parse XML; XLS ouverture LibreOffice et export CSV de controle). Controle visuel ponctuel uniquement, pas revue juridique exhaustive des milliers de pages.',
 '- HTTP 404 sur certains identifiants de service Cellar, mais pas preuve de disparition des sources EUR-Lex. Distinguer ces endpoints, les HTTP 403 Legifrance, les reponses vides et les pannes navigateur. Les sources legales accessibles au navigateur ne sont pas declarees mortes.',
 f'- D19 est un PDF images, original conserve mais OCR requis; aucun moteur OCR disponible dans cet environnement. Les {len(ok)-1} autres documents valides sont techniquement exploitables, sous reserve de curation des contenus hors perimetre et historiques.',
 '- Doublons binaires: '+str(len(duplicates))+'. Une empreinte detecte les fichiers identiques, pas les textes partiellement redondants entre FAQ, notice et guide.',
 ]
(ROOT/'metadata/bilan.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
