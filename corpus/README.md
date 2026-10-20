# Corpus EMEBI / ITGS

Corpus de 40 documents constitué le 5 octobre 2026 pour amorcer un POC de recherche augmentée (RAG) consacré à l'enquête mensuelle sur les échanges de biens intra-UE (EMEBI) en France et aux statistiques du commerce international de biens (ITGS).

## Contenu

- `01_france_emebi` : notice EMEBI 2026, documentation DEBWEB/DTI, variables obligatoires et calendrier.
- `02_union_europeenne` : règlements européens d'origine et versions consolidées applicables, ainsi que les manuels Eurostat.
- `03_international_itgs` : recommandations et manuel de compilation des Nations unies.
- `04_historique_deb_emebi` : documentation utile à la transition DEB vers EMEBI.
- `metadata/catalogue.csv` : provenance, statut, priorité et empreinte de chaque document.
- `metadata/documents_non_telecharges.csv` : références pertinentes qui n'ont pas pu être téléchargées automatiquement.

## Points d'attention

- Les versions consolidées d'EUR-Lex sont des outils documentaires. Les actes publiés au Journal officiel de l'Union européenne restent les versions juridiquement authentiques.
- L'accès public à un document ne signifie pas nécessairement qu'il est placé sous licence ouverte. Les droits de réutilisation doivent être validés avant diffusion du corpus hors du cadre du POC.
- Les pages HTML ont été conservées comme instantanés de consultation. Pour l'indexation, il conviendra d'en extraire le contenu principal et d'éliminer menus, scripts et éléments de navigation.
- Les documents français opérationnels distinguent l'EMEBI, de nature statistique, de l'état récapitulatif TVA, de nature fiscale.

## Préparation RAG recommandée

Conserver les PDF originaux, extraire le texte page par page, associer chaque segment à l'identifiant du catalogue, au numéro de page, au niveau juridique, à la période d'application et à l'URL source. Donner la priorité aux documents marqués `essentielle`. Ne pas mélanger dans une même réponse les règles en vigueur et la documentation historique.
