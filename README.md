# EMEBI / ITGS RAG pilot

Ce dépôt prépare un pilote d'extraction documentaire et de recherche augmentée (RAG) consacré :

- à l'enquête mensuelle sur les échanges de biens intra-Union européenne (EMEBI) en France ;
- au cadre européen et international des statistiques du commerce international de biens (ITGS).

## État du projet

Le projet est actuellement au stade de constitution et de qualification du corpus. Aucun pipeline d'extraction n'est encore implémenté et aucun mini-corpus expérimental n'est encore arrêté.

Le corpus de travail local comprend 40 documents officiels provenant principalement de la DGDDI, d'EUR-Lex, d'Eurostat et de la Division de statistique des Nations unies.

## Gestion du corpus

Les documents téléchargés ne sont pas redistribués dans ce dépôt. Les PDF, copies HTML et archives restent dans l'environnement de travail local et sont exclus de Git.

Le fichier [`corpus/metadata/catalogue.csv`](corpus/metadata/catalogue.csv) constitue le manifeste de référence. Il décrit notamment, pour chaque document :

- son identifiant stable ;
- son titre et son organisme producteur ;
- son URL officielle ;
- son nom de fichier local ;
- sa version et son statut ;
- son empreinte SHA-256 ;
- sa priorité et son caractère actuel ou historique.

L'accès public à un document ne signifie pas automatiquement qu'il est placé sous licence ouverte. Chaque source conserve ses propres conditions d'utilisation et de réutilisation.

## Structure versionnée

```text
corpus/
  README.md
  metadata/
    catalogue.csv
    documents_non_telecharges.csv
```

Les répertoires `work/` et `outputs/`, les documents sources et les résultats expérimentaux sont volontairement exclus du dépôt. Un mécanisme unique de reconstitution du corpus remplacera ultérieurement les listes de téléchargement provisoires.

## Reproductibilité

L'empreinte SHA-256 inscrite dans le catalogue permet de vérifier qu'un fichier récupéré correspond exactement au document qualifié lors de la constitution du corpus. Le futur mécanisme de téléchargement devra utiliser le catalogue comme source de vérité et signaler toute indisponibilité ou divergence d'empreinte.

## Licence

Le code et la documentation propres à ce dépôt sont publiés sous licence MIT. Cette licence ne s'applique pas aux documents tiers référencés dans le catalogue.
