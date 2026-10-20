"""Selection de 45 documents officiels; valeurs inconnues laissees vides."""
from urllib.parse import quote

D = 'https://www.douane.gouv.fr/'
E = 'https://eur-lex.europa.eu/legal-content/FR/'
U = 'https://unstats.un.org/'
FOLDERS = ['01_france_emebi', '02_union_europeenne', '03_international_itgs', '04_historique_deb_emebi', '05_nomenclatures_et_referentiels']
DOCS = []

def add(group, year, org, slug, title, source, direct='', fmt='html', theme='', kind='documentation operationnelle', lang='fr', status='Sans portee normative autonome', period='', historical=False, priority='utile', selector='', publication='', version=''):
    DOCS.append(dict(id=f'D{len(DOCS)+1:02d}', titre=title, organisme=org,
        niveau='international' if group == 3 else 'UE' if group == 2 or org in ('Union europeenne', 'Eurostat') else 'France',
        type_document=kind, theme=theme, date_publication=publication, date_version=version,
        statut_juridique=status, periode_application=period, langue=lang,
        url_source=source, url_telechargement=direct, date_consultation='',
        nom_fichier=f'{FOLDERS[group-1]}/{year}_{org.lower().replace(" ", "_")}_{slug}_{lang}.{fmt}',
        format=fmt, nombre_pages='', sha256='', licence_ou_conditions='conditions a verifier', libre_acces='',
        priorite_rag=priority, historique_ou_actuel='historique' if historical else 'actuel',
        resume=theme, observations='', selector=selector, resultat='a_traiter'))

guide=D+'fiche/comment-remplir-sa-reponse-lenquete-mensuelle-statistique-sur-les-echanges-de-biens-intra-ue'
demarche=D+'demarche/repondre-lenquete-statistique-sur-les-echanges-de-biens-au-sein-de-lunion-europeenne-emebi'
service=D+'service-en-ligne/echanges-intra-ue-de-biens-debweb2-ex-deb'
add(1,2026,'DGDDI','notice_emebi','Note de reference EMEBI 2026',guide,D+'sites/default/files/2025-12/22/'+quote('Notice EMEBI 2026 version 19 décembre 2025.pdf'), 'pdf','Obligations, echantillon, variables, pays, valeur statistique, corrections',priority='essentielle',period='2026',version='2025-12-19')
add(1,2026,'DGDDI','remplir_emebi','Comment remplir sa reponse EMEBI',guide,theme='Variables, nomenclatures, nature de transaction, valeur statistique',priority='essentielle')
add(1,2026,'DGDDI','repondre_emebi','Repondre a l enquete statistique EMEBI',demarche,theme='Entreprises concernees, selection, obligations',priority='essentielle')
add(1,2026,'DGDDI','faq_emebi_tva','FAQ EMEBI et etat recapitulatif TVA',D+'fiche/faq-et-tutoriels-videos-lenquete-statistique-sur-les-echanges-de-biens-intra-ue-et-letat',theme='Distinction EMEBI et TVA, cas pratiques',priority='essentielle')
add(1,2026,'DGDDI','calendrier_emebi','Calendrier des reponses EMEBI',D+'fiche/calendrier-des-reponses-lenquete-mensuelle-statistique-sur-les-echanges-de-biens-intra-ue',theme='Echeances mensuelles',period='2026',priority='essentielle')
add(1,2025,'DGDDI','manuel_dti','Manuel utilisateurs DEBWEB2 mode DTI EMEBI et TVA',service,D+'sites/default/files/2025-08/26/Manuel_utilisateurs_DEBWEB_DTI_EMEBI_recapitulatif_TVA_v1.0.pdf','pdf','Saisie et corrections EMEBI et TVA',version='1.0')
add(1,2022,'DGDDI','manuel_xml','Documentation import XML DTI+',service,D+'sites/default/files/2022-02/15/DEB%20_Manuel_mode_DTI%2B_Xml_v1.3.8.pdf','pdf','Format technique XML, controles des variables',version='1.3.8')
add(1,2022,'DGDDI','schema_xml','Schema XSD des imports DEBWEB2',service,D+'sites/default/files/2022-02/24/Sch%C3%A9maXSD.xsd','xsd','Validation technique des fichiers XML',kind='schema technique',lang='mul')
add(1,2022,'DGDDI','manuel_dtiplus','Manuel utilisateurs DTI+',service,D+'sites/default/files/2022-02/07/Manuel_utilisateurs_mode_DTIplus_v5.1.6.pdf','pdf','Import et controles DEBWEB2',version='5.1.6')
add(4,2020,'DGDDI','rectifications_deb','Manuel rectifications et suppressions DEB',service,D+'sites/default/files/uploads/files/2020-02/Manuel%20utilisateurs%20Rectifications%20suppressions%20DEB.pdf','pdf','Corrections des anciennes DEB',historical=True,status='Documentation historique DEB; ne pas appliquer a EMEBI sans verification')
add(1,1951,'Legifrance','loi_secret_statistique','Loi 51-711 du 7 juin 1951 obligation coordination et secret statistiques','https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000888573/',theme='Obligation de reponse, secret statistique',kind='loi',status='Version consolidee a verifier au 2026-10-06',priority='essentielle',publication='1951-06-07')
add(1,2025,'Legifrance','programme_enquetes_2026','Arrete du 27 octobre 2025 programme enquetes statistiques 2026','https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000052835965',theme='Programme statistique, caractere obligatoire EMEBI',kind='arrete et annexe',status='Texte publie au JO; application 2026 a verifier',period='2026',publication='2025-10-27',priority='essentielle')
add(1,2024,'CNIS','avis_conformite_emebi','Avis de conformite EMEBI', 'https://www.cnis.fr/wp-content/uploads/2024/10/ac-2024-dgddi-emebi-mensuelle.pdf','https://www.cnis.fr/wp-content/uploads/2024/10/ac-2024-dgddi-emebi-mensuelle.pdf','pdf','Label, echantillonnage, obligations',kind='avis de conformite',priority='essentielle')
add(1,2024,'INSEE','methode_emebi','Courrier des statistiques numero 12 article EMEBI','https://www.insee.fr/fr/information/8264548?sommaire=8264562','https://www.insee.fr/fr/statistiques/fichier/8264562/INSEE_CS12.pdf','pdf','Refonte DEB, echantillon et production statistique',kind='article methodologique',priority='essentielle')

def eu(year,slug,title,celex,theme,version='',historical=False):
    add(2 if not historical else 4,year,'Union europeenne',slug,title,E+'ALL/?uri=CELEX:'+celex,
        E+'TXT/PDF/?uri=CELEX:'+celex,'pdf',theme,kind='reglement',status='Abroge au 2022-01-01; usage historique uniquement' if historical else 'Texte ou consolidation; applicabilite et modifications a verifier',historical=historical,priority='essentielle',version=version)
eu(2019,'reglement_2152','Reglement UE 2019/2152 statistiques europeennes entreprises','02019R2152-20260510','Cadre EBS, intra-UE et extra-UE, confidentialite','2026-05-10')
eu(2020,'reglement_1197','Reglement execution UE 2020/1197','02020R1197-20260305','Variables ITGS, qualite et echanges microdonnees','2026-03-05')
eu(2021,'reglement_1704','Reglement delegue UE 2021/1704','32021R1704','Informations statistiques a fournir par autorites fiscales et douanieres')
eu(2026,'reglement_0047','Reglement delegue UE 2026/47','32026R0047','Modification EBS et actes delegues dont 2021/1704')
eu(2009,'reglement_0223','Reglement CE 223/2009 statistiques europeennes','02009R0223-20241226','Secret statistique, qualite et diffusion','2024-12-26')
add(2,2017,'Eurostat','code_bonnes_pratiques','Code de bonnes pratiques statistiques europeennes', 'https://ec.europa.eu/eurostat/web/products-catalogues/-/ks-02-18-142','https://ec.europa.eu/eurostat/documents/4031688/9332274/KS-02-18-142-FR-N.pdf/130905e7-45a7-4475-b37c-8f699b5e33e1?t=1540215834000','pdf','Qualite, confidentialite, independance',kind='code de bonnes pratiques',version='2017')
for slug,title,code in [('guide_utilisateurs','User guide on European statistics on international trade in goods','ks-01-26-012-en-n'),('manuel_detaille','European business statistics compilers manual for detailed ITGS','ks-01-26-006'),('manuel_agrege','European business statistics compilers manual for aggregated ITGS','ks-01-26-002'),('manuel_tec','European business statistics compilers manual trade by enterprise characteristics 2025 edition','ks-01-25-068'),('manuel_tic','European business statistics compilers manual trade by invoicing currency','ks-01-26-003')]:
    add(2,2025 if slug=='manuel_tec' else 2026,'Eurostat',slug,title,'https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/w/'+code,fmt='pdf',theme='Methodologie ITGS intra-UE et extra-UE, qualite et diffusion' if slug not in ('manuel_tec','manuel_tic') else 'Statistiques par caracteristiques entreprises' if slug=='manuel_tec' else 'Monnaie de facturation',kind='manuel methodologique',lang='en',priority='essentielle' if slug in ('guide_utilisateurs','manuel_detaille') else 'utile',selector=code.upper())
add(2,2025,'Eurostat','metadonnees_itgs','International trade in goods reference metadata','https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_agg_esms.htm',theme='Couverture intra-UE et extra-UE, revision, confidentialite, qualite',kind='metadonnees',lang='en')

add(3,2026,'ONU','imts_2026','International Merchandise Trade Statistics Concepts and Definitions IMTS 2026 White Cover','https://unstats.un.org/Unsd/trade/events/2026/Abuja-IMTS2026/default.asp',U+'UNSDWebsite/statcom/session_57/documents/BG-3h-1-International_Merchandise_Trade_Statistics_Concepts_and_Definitions-IMTS_2026-E.pdf','pdf','Recommandations ITGS, territoire, valorisation et partenaires',kind='recommandations internationales',lang='en',status='Recommandations non contraignantes; White Cover 2026',priority='essentielle')
add(3,2026,'ONU','rapport_commission_57','Report Statistical Commission 57th session E/2026/24 E/CN.3/2026/35','https://digitallibrary.un.org/record/4109670',U+'UNSDWebsite/statcom/session_57/documents/2026-35-FinalReport-E.pdf','pdf','Decisions Commission statistique concernant IMTS 2026',kind='rapport institutionnel',lang='en',status='Rapport et decisions; non reglementaire')
add(3,2010,'ONU','imts_2010','International Merchandise Trade Statistics Concepts and Definitions 2010',U+'unsd/trade/imts/methodology.asp',U+'unsd/trade/eg-imts/IMTS%202010%20%28English%29.pdf','pdf','Base historique internationale ITGS',kind='recommandations internationales',lang='en',status='Recommandations non contraignantes; edition historique 2010',historical=True,publication='2011',priority='essentielle')
add(3,2013,'ONU','manuel_compilateurs_rev1','International Merchandise Trade Statistics Compilers Manual Revision 1',U+'unsd/trade/imts/methodology.asp',U+'unsd/trade/publications/seriesf_87Rev1_e_cover.pdf','pdf','Collecte, compilations, qualite et diffusion ITGS',kind='manuel methodologique',lang='en',status='Manuel non contraignant fonde sur IMTS 2010',publication='2013')
add(3,2008,'ONU','supplement_compilateurs','Supplement to IMTS Compilers Manual 2008',U+'unsd/trade/imtssupplcompilersmanual.htm',fmt='pdf',theme='Methodologie historique ITGS',kind='manuel methodologique',lang='en',historical=True,status='Supplement historique non contraignant',selector='pdf')
add(3,2025,'ONU','hibts','Handbook on Integrating Business and Trade Statistics White Cover',U+'unsd/trade/events/2025/Santiago/default.asp',U+'UNSDWebsite/statcom/session_56/documents/BG-3k-HIBTS_White_Cover_Version-E.pdf','pdf','Integration statistiques entreprises et commerce de biens',kind='manuel methodologique',lang='en',status='Manuel non contraignant; White Cover 2025')

add(4,2021,'DGDDI','transition_deb_emebi','DEB changements declaratifs a compter du 1er janvier 2022',D+'actualites/deb-changements-declaratifs-relatifs-aux-echanges-de-biens-intra-ue-compter-du-1er',theme='Separation enquete EMEBI et etat recapitulatif TVA',historical=True,priority='essentielle',period='Transition 2022')
add(4,2022,'Legifrance','decret_0126','Decret 2022-126 du 4 fevrier 2022','https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045123988',theme='Transition DEB, etat recapitulatif TVA',kind='decret',status='Texte original; effet sur periodes a compter du 2022-01-01',historical=True,priority='essentielle',publication='2022-02-04')
add(4,2026,'Legifrance','cgi_289b','Code general des impots article 289 B','https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191662',theme='Etat recapitulatif TVA; distinct EMEBI',kind='code consolide',status='Version et date d effet de l abrogation annoncee a verifier',priority='essentielle')
add(4,2026,'Legifrance','cgi_annexe_96j_96m','Code general des impots annexe III articles 96 J a 96 M','https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069574/LEGISCTA000006179449/',theme='Dispositions declaratives TVA et historique DEB',kind='code consolide',status='Versions article par article a verifier; ne pas appliquer les dispositions abrogees')
eu(2004,'reglement_0638_historique','Reglement CE 638/2004 ancien cadre Intrastat','32004R0638','Ancien cadre statistiques intra-UE',historical=True)
eu(2009,'reglement_0471_historique','Reglement CE 471/2009 ancien cadre extra-UE','02009R0471-20161223','Ancien cadre statistiques extra-UE','2016-12-23',historical=True)

add(5,2025,'Union europeenne','nomenclature_combinee_2026','Reglement execution UE 2025/1926 nomenclature combinee 2026',E+'ALL/?uri=CELEX:32025R1926',E+'TXT/PDF/?uri=CELEX:32025R1926','pdf','NC8 et tarif douanier commun 2026',kind='reglement et nomenclature',status='Texte JO; nomenclature applicable 2026',period='2026',priority='essentielle')
add(5,2026,'DGDDI','nc8_2026','Nomenclature combinee NC8 2026 libelles officiels',D+'fiche/la-nomenclature-combinee-nc8-et-la-nomenclature-generale-des-produits-ngp',fmt='xls',theme='Codes produits et libelles officiels NC8',kind='referentiel',period='2026',priority='essentielle',selector='2026|officiel')
add(5,2020,'Union europeenne','geonomenclature','Reglement execution UE 2020/1470 nomenclature pays et territoires',E+'ALL/?uri=CELEX:32020R1470',E+'TXT/PDF/?uri=CELEX:32020R1470','pdf','Pays partenaires et codes pays',kind='reglement et referentiel',status='Texte JO; applicabilite actuelle a verifier',priority='essentielle')
add(5,2026,'Eurostat','manuel_geonomenclature','Geonomenclature applicable to European ITGS 2026 edition','https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/w/ks-01-26-020-en-n',fmt='pdf',theme='Pays et territoires partenaires',kind='manuel methodologique',lang='en',selector='KS-01-26-020')
add(5,2026,'DGDDI','elaboration_statistiques','Elaboration des statistiques du commerce exterieur','https://lekiosque.finances.gouv.fr/site_fr/etudes/methode/elaboration.asp',theme='Sources EMEBI et douane extra-UE, compilation et diffusion',kind='note methodologique')
add(5,2026,'DGDDI','qualite_statistiques','Qualite des statistiques du commerce exterieur','https://lekiosque.finances.gouv.fr/site_fr/etudes/methode/qualite.asp',theme='Echantillon, qualite, revisions et diffusion',kind='note methodologique')
add(5,2026,'DGDDI','ngp_2026','Nomenclature generale des produits NGP 2026',D+'fiche/la-nomenclature-combinee-nc8-et-la-nomenclature-generale-des-produits-ngp',fmt='xls',theme='Referentiel produits complementaire NC8',kind='referentiel',period='2026',selector='2026|ngp')
assert len(DOCS) == 45, len(DOCS)
