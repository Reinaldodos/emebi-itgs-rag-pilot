# Corpus EMEBI et statistiques du commerce international de biens

## Périmètre

Corpus documentaire pour un POC de RAG, constitué le 6 octobre 2026 à partir de
45 documents sélectionnés. L'état exact de la collecte, ses échecs et les
répartitions figurent dans [le bilan](metadata/bilan.md). Il s'agit d'une livraison
partielle tant que des originaux prioritaires restent indisponibles.

Trois cadres doivent rester distincts dans les réponses :

- **EMEBI France** : enquête statistique mensuelle sur les échanges de biens
  intra-UE, auprès des entreprises sélectionnées. Ne pas déduire un seuil
  déclaratif universel des descriptions d'échantillon.
- **État récapitulatif TVA** : obligation fiscale distincte de l'enquête, même si
  DEBWEB2 peut préparer un brouillon à partir d'une réponse statistique.
- **ITGS** : cadre européen intra-UE et extra-UE, et recommandations internationales
  ONU non contraignantes. L'EMEBI n'est pas une déclaration extra-UE.

Les thèmes couverts sont les obligations, la sélection, les échéances, les
variables, les produits et pays partenaires, la nature de transaction, les valeurs,
les corrections, la confidentialité, la qualité et la diffusion.

## Sources et arborescence

Priorité à DGDDI/Douane, DSECE/Le Kiosque, INSEE, Comité du label/CNIS,
Légifrance, EUR-Lex, Eurostat/Commission et Division statistique des Nations unies.
Une copie réglementaire sur le site d'un institut statistique public peut servir
de repli ; le catalogue identifie séparément la source normative et le téléchargement.

```text
corpus/
  01_france_emebi/                 notices, FAQ, échéances, guides techniques, loi
  02_union_europeenne/             cadre EBS/ITGS, manuels et métadonnées
  03_international_itgs/           IMTS, manuels et décisions de la Commission ONU
  04_historique_deb_emebi/          transition, DEB ancienne et dispositions TVA
  05_nomenclatures_et_referentiels/ NC8, NGP, pays, élaboration et qualité
  metadata/                       catalogues CSV/JSON, état, exclusions, échecs, bilan
  logs/                           tentatives, sources HTML brutes, contrôles, textes PDF
```

Les noms suivent `AAAA_organisme_titre_court_langue.ext`, sans accents. L'année
est celle de l'édition quand elle est établie, sinon celle de la capture. Elle ne
remplace pas une date de publication : les champs inconnus restent vides. Un
millésime dans l'URL n'est pas une preuve de version du contenu. `fr`, `en`, `mul`
désignent français, anglais et schéma technique multilingue.

## Collecte par passes et contrôle

Première passe : une tentative par candidat, sans retry interne. Les passes
suivantes portent seulement sur les échecs : résolution des pièces jointes,
normalisation de liens équivalents, autre format officiel, navigateur ordinaire,
puis autre lien original vérifié. Trois requêtes simultanées au maximum pour les
lots HTTP ; connexion limitée à 12 secondes et lecture à 35 secondes. Un échec
n'interrompt pas le lot. Les succès sont sauvegardés après chaque document.

Un refus d'accès n'est pas contourné. Un lien sans nouvelle méthode sûre est
laissé en échec, avec son motif. Aucun résultat de recherche ni écran de contrôle
d'accès ne constitue un document. Un timeout navigateur peut précéder l'arrivée
effective d'un fichier : seul le fichier local contrôlé est compté.

Les PDF et XLS sont conservés sans réécriture. Les HTML sont nettoyés des
scripts, formulaires et principaux éléments de navigation ; l'original brut est
conservé pour audit. Chaque HTML comporte le titre, l'URL et la date de consultation.
Tous les fichiers retenus sont rouverts et associés à une empreinte SHA-256. Les
PDF passent `pdfinfo` et l'extraction intégrale `pdftotext`, les XLS sont ouverts
par LibreOffice, les HTML et XSD sont parsés. Le contrôle visuel est ponctuel,
et non une revue de chaque page. Les copies de contrôle ne sont pas des documents
supplémentaires du corpus. Le règlement 223/2009 obtenu en repli (D19) est un
PDF-images : original conservé, OCR requis mais non produit faute de moteur
installé. Ne pas le considérer comme directement indexable. Une page image
isolée dans les autres PDF peut également nécessiter un traitement ultérieur.

Le catalogue CSV UTF-8 utilise la virgule et les règles CSV de citation ; JSON
reprend exactement les mêmes champs et valeurs. Il contient uniquement les
documents validés. `etat_collecte.json` contient les 45 candidats, y compris les
échecs. `documents_non_retenus.csv` distingue exclusions éditoriales et échecs
techniques, qui figurent dans `documents_en_echec.csv`.

## Utilisation RAG et limites

Indexer les cinq dossiers documentaires, pas `logs/` ni les catalogues comme
sources métier. Conserver l'identifiant, l'URL, le cadre, le millésime, le statut
historique et le numéro de page pour chaque fragment. Filtrer les articles hors
commerce extérieur dans le numéro complet du Courrier des statistiques. Séparer
les calendriers et nomenclatures historiques présents dans les pages courantes.

Ne jamais répondre à une question actuelle avec un texte abrogé sans l'annoncer.
Les consolidations EUR-Lex sont des outils documentaires : seuls les actes
authentiques du Journal officiel font foi. IMTS 2026 a été adopté selon la
décision 57/108 ; le fichier acquis reste une version White Cover à réviser.
Les guides techniques 2022 toujours proposés par la Douane doivent être distingués
de la notice annuelle 2026.

La base fiscale française après recodification de 2026 nécessite une validation
juridique : l'article 289 B affiche une note d'abrogation au 1er septembre 2026
avec exceptions. Ne pas le présenter comme la base actuelle validée. Vérifier
aussi les originaux normatifs manquants avant une utilisation de conformité.

L'accès gratuit ne donne pas une licence ouverte. Les autorisations explicites
sont consignées par document, notamment CC-BY 4.0 Eurostat avec exceptions de
droits tiers ; les publications ONU peuvent rester tous droits réservés.
En l'absence de preuve, la mention est « conditions à vérifier ». Valider les
droits avant redistribution ou mise à disposition publique du POC.

## Reprise locale

Le collecteur est dans `../src/collect_corpus.py` et nécessite Python, `requests`,
BeautifulSoup, Poppler et LibreOffice. Il préserve les succès existants :

```bash
/usr/bin/python3 src/collect_corpus.py --pass-number 2
/usr/bin/python3 src/import_browser_document.py D16 /chemin/original.pdf --url URL_OFFICIELLE
/usr/bin/python3 src/finalize_corpus.py
```

Les permissions réseau de la session restent gérées par l'environnement. Les
commandes ne les modifient pas. Ne pas relancer une passe déjà sans alternative
valide ; importer un original obtenu légalement, puis refaire les contrôles.
