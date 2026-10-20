# EMEBI / ITGS RAG pilot

Ce dépôt prépare un pilote reproductible de collecte, d'extraction et de structuration documentaire consacré :

- à l'enquête mensuelle sur les échanges de biens intra-Union européenne (EMEBI) en France ;
- au cadre européen et international des statistiques du commerce international de biens (ITGS) ;
- à la préparation ultérieure d'un POC de recherche augmentée (RAG).

## État du projet

Le projet contient actuellement :

- une chaîne Python de collecte, de contrôle et de finalisation du corpus ;
- une première chaîne d'extraction et de parsing ;
- des tests automatisés pour la collecte et le parsing ;
- un catalogue de 37 documents validés parmi 45 candidats qualifiés.

Le prochain travail expérimental portera sur la définition d'un mini-corpus homogène et sur la comparaison contrôlée des méthodes d'extraction. Cette étape n'est pas encore engagée dans l'historique Git.

## Structure

```text
src/                 collecte, import, contrôle, extraction et parsing
tests/               tests automatisés
corpus/README.md     périmètre, méthode de collecte et limites
corpus/metadata/     catalogue, état de collecte, bilan et exclusions
corpus/<catégorie>/  documents sources locaux, exclus de Git
data/                résultats générés, exclus de Git
```

## Gestion du corpus

Les PDF, pages HTML, feuilles Excel et autres documents téléchargés ne sont pas redistribués dans ce dépôt. Ils restent dans l'environnement local et conservent les conditions d'utilisation de leurs producteurs.

Le fichier [`corpus/metadata/catalogue.csv`](corpus/metadata/catalogue.csv) constitue le manifeste des documents validés. Il conserve notamment leurs identifiants, sources officielles, versions, noms locaux et empreintes SHA-256. Le fichier `etat_collecte.json` conserve l'état des 45 candidats, y compris les échecs.

L'accès gratuit à un document ne signifie pas qu'il est placé sous licence ouverte. La licence MIT de ce dépôt couvre uniquement le code et la documentation propres au projet.

## Documentation du corpus

Le périmètre métier, la méthode de collecte, les contrôles appliqués et les limites connues sont décrits dans [`corpus/README.md`](corpus/README.md). Un bilan détaillé est disponible dans [`corpus/metadata/bilan.md`](corpus/metadata/bilan.md).

## Licence

Le code et la documentation propres à ce dépôt sont publiés sous licence MIT. Les documents tiers référencés dans le catalogue restent soumis à leurs propres droits.
