# Bilan du corpus

Controle du 2026-10-06. Livraison partielle: 37 documents valides sur 45 selectionnes; 8 originaux restent a obtenir.

Inventaire: 51 documents examines, dont 45 candidats retenus et 6 exclus. Les aliases de liens ne sont pas comptes comme documents.

## Repartition des documents valides

- niveau: France: 18, UE: 13, international: 6
- organisme: DGDDI: 15, Legifrance: 1, Comite du label (INSEE): 1, INSEE: 1, Union europeenne: 5, Eurostat: 8, ONU: 6
- type_document: documentation operationnelle: 10, schema technique: 1, loi: 1, avis de conformite: 1, article methodologique: 1, reglement: 4, code de bonnes pratiques: 1, manuel methodologique: 9, metadonnees: 1, recommandations internationales: 2, rapport institutionnel: 1, referentiel: 2, reglement et referentiel: 1, note methodologique: 2
- langue: fr: 23, mul: 1, en: 13
- format: pdf: 25, html: 9, xsd: 1, xls: 2

## Dix documents prioritaires disponibles

1. D01 — [Note de reference EMEBI 2026](../01_france_emebi/2026_dgddi_notice_emebi_fr.pdf) : Obligations, echantillon, variables, pays, valeur statistique, corrections.
2. D03 — [Repondre a l enquete statistique EMEBI](../01_france_emebi/2026_dgddi_repondre_emebi_fr.html) : Entreprises concernees, selection, obligations.
3. D04 — [FAQ EMEBI et etat recapitulatif TVA](../01_france_emebi/2026_dgddi_faq_emebi_tva_fr.html) : Distinction EMEBI et TVA, cas pratiques.
4. D05 — [Calendrier des reponses EMEBI](../01_france_emebi/2026_dgddi_calendrier_emebi_fr.html) : Echeances mensuelles.
5. D11 — [Loi 51-711 du 7 juin 1951 obligation coordination et secret statistiques](../01_france_emebi/1951_legifrance_loi_secret_statistique_fr.html) : Obligation de reponse, secret statistique.
6. D13 — [Avis de conformite EMEBI](../01_france_emebi/2024_cnis_avis_conformite_emebi_fr.pdf) : Label, echantillonnage, obligations.
7. D15 — [Reglement UE 2019/2152 statistiques europeennes entreprises](../02_union_europeenne/2019_union_europeenne_reglement_2152_fr.pdf) : Cadre EBS, intra-UE et extra-UE, confidentialite.
8. D16 — [Reglement execution UE 2020/1197](../02_union_europeenne/2020_union_europeenne_reglement_1197_fr.pdf) : Variables ITGS, qualite et echanges microdonnees.
9. D22 — [European business statistics compilers manual for detailed ITGS](../02_union_europeenne/2026_eurostat_manuel_detaille_en.pdf) : Methodologie ITGS intra-UE et extra-UE, qualite et diffusion.
10. D27 — [International Merchandise Trade Statistics Concepts and Definitions IMTS 2026 White Cover](../03_international_itgs/2026_onu_imts_2026_en.pdf) : Recommandations ITGS, territoire, valorisation et partenaires.

## Originaux manquants

- D12 — Arrete du 27 octobre 2025 programme enquetes statistiques 2026: Replis officiels disponibles epuises; import manuel requis
- D17 — Reglement delegue UE 2021/1704: 404 Client Error:  for url: https://publications.europa.eu/resource/consolidation/02021R1704-20260510
- D18 — Reglement delegue UE 2026/47: 404 Client Error:  for url: https://publications.europa.eu/resource/oj/L_202600047
- D34 — Decret 2022-126 du 4 fevrier 2022: Replis officiels disponibles epuises; import manuel requis
- D35 — Code general des impots article 289 B: Replis officiels disponibles epuises; import manuel requis
- D36 — Code general des impots annexe III articles 96 J a 96 M: Replis officiels disponibles epuises; import manuel requis
- D38 — Reglement CE 471/2009 ancien cadre extra-UE: 404 Client Error:  for url: https://publications.europa.eu/resource/consolidation/02009R0471-20161223
- D39 — Reglement execution UE 2025/1926 nomenclature combinee 2026: Replis officiels disponibles epuises; import manuel requis

## Lacunes et validations requises

- Priorite de complement: arrete 2026, reglement 2021/1704 consolide, acte modificatif 2026/47 et nomenclature combinee normative 2026. Le reglement 2020/1197 consolide et la geonomenclature normative ont ete recuperes. Les manuels ne remplacent pas les textes manquants.
- Reconstituer la base fiscale TVA apres recodification 2026. Article 289 B: affichage de version en vigueur et nota d abrogation au 1er septembre 2026 avec exceptions; ne pas l utiliser comme base actuelle sans avis juridique.
- Confirmer avec DGDDI le plan annuel de selection EMEBI et la portee des chiffres descriptifs CNIS; obligation liee a la selection/notification, pas a un seuil universel deduit d un avis.
- Confirmer le maintien des guides techniques 2022 toujours lies sur la page courante. Les versions du contenu different parfois du nom du fichier.
- IMTS 2026: recommandations adoptees (D28, decision 57/108), mais original acquis White Cover soumis a revision editoriale; confirmer calendrier national de mise en oeuvre.
- Verifier droits de reutilisation pour indexation, redistribution et publication RAG, surtout documents ONU tous droits reserves et photos tiers. Acces public ne signifie pas licence ouverte.
- Videos Douane non transcrites, tables de passage annuelles NC8 non retenues, liste de l echantillon individuel non publique. Ces lacunes ne sont pas masquees par des donnees fabriquees.
- Controle technique de tous les fichiers (PDF pdfinfo et extraction integrale pdftotext; HTML parse; XSD parse XML; XLS ouverture LibreOffice et export CSV de controle). Controle visuel ponctuel uniquement, pas revue juridique exhaustive des milliers de pages.
- HTTP 404 sur certains identifiants de service Cellar, mais pas preuve de disparition des sources EUR-Lex. Distinguer ces endpoints, les HTTP 403 Legifrance, les reponses vides et les pannes navigateur. Les sources legales accessibles au navigateur ne sont pas declarees mortes.
- D19 est un PDF images, original conserve mais OCR requis; aucun moteur OCR disponible dans cet environnement. Les 36 autres documents valides sont techniquement exploitables, sous reserve de curation des contenus hors perimetre et historiques.
- Doublons binaires: 0. Une empreinte detecte les fichiers identiques, pas les textes partiellement redondants entre FAQ, notice et guide.
