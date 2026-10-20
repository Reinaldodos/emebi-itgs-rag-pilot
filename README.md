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

## Installation reproductible

Prérequis : Python **3.11 ou supérieur** et [uv](https://docs.astral.sh/uv/getting-started/installation/).
L'environnement verrouillé est vérifié avec Python 3.13. Depuis la racine du dépôt :

```bash
uv sync --locked --python 3.13
uv run --locked python -c "import requests, bs4, pymupdf"
uv run --locked pytest
```

`uv sync` crée un environnement isolé `.venv/` et installe par défaut le groupe
`dev`, qui contient pytest. `pyproject.toml` déclare les versions minimales des
dépendances directes ; `uv.lock` fixe les versions et empreintes des dépendances
directes et transitives. `--locked` refuse un manifeste incompatible avec le verrou.
Pour installer uniquement les dépendances d'exécution, utiliser
`uv sync --locked --no-dev --python 3.13`. Le dépôt reste un projet de scripts,
sans package Python à construire ; exécuter les commandes depuis sa racine.

Avec GNU Make, `make setup` et `make test` sont les raccourcis respectifs de
`uv sync --locked` et `uv run --locked pytest`. Pour mettre à jour volontairement
les dépendances, exécuter `uv lock --upgrade`, puis `uv sync --locked` et les tests,
et versionner ensemble le manifeste et le verrou.

### Outils système

Les dépendances Python sont `requests` (HTTP), `beautifulsoup4` (HTML) et
`pymupdf` (extraction PDF). Elles ne remplacent pas les exécutables utilisés
par la validation du corpus :

| Exécutables | Utilisation | Paquet Debian / Ubuntu |
| --- | --- | --- |
| `pdfinfo`, `pdftotext` | Contrôle des PDF et export de leur texte dans `src/collect_corpus.py` | `poppler-utils` |
| `libreoffice` | Ouverture et conversion de contrôle des fichiers Excel, en mode sans interface | `libreoffice-calc` |

Installer ces outils avec le gestionnaire système, par exemple :

```bash
sudo apt-get install poppler-utils libreoffice-calc
pdfinfo -v
pdftotext -v
libreoffice --version
```

Leurs versions sont gérées par la distribution, séparément de `uv.lock`.
Ils ne sont nécessaires que pour les chemins de validation correspondants ;
les tests unitaires de collecte utilisent des réponses locales sans téléchargement.
Les tests de parsing utilisent actuellement le PDF local
`corpus/02_union_europeenne/2019_union_europeenne_reglement_2152_fr.pdf`,
exclu de Git : sans ce document, les imports et la collecte des tests fonctionnent,
mais l'exécution des tests de parsing échoue. Voir la
[documentation du corpus](corpus/README.md) pour la gestion des sources.

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

## Extraction et parsing

Les deux scripts acceptent `--input chemin/vers/source.pdf` et `--output chemin/vers/resultat`.
Les chemins relatifs sont interprétés depuis le répertoire de travail. Sans `--input`,
ils utilisent le règlement 2019/2152 attendu dans le corpus local, qui n'est pas distribué
avec le dépôt.

```bash
python src/01_extract.py --input /chemin/source.pdf
python src/02_parse.py --input /chemin/reglement-2152.pdf --output data/structured/reglement.json
```

Sans `--output`, ou avec `--output -`, le résultat est envoyé vers stdout sans créer de
fichier. Pour le parsing, stdout contient uniquement le JSON ; le résumé est envoyé vers
stderr. Une sortie existante est refusée, sauf avec `--force`. Même avec cette option,
le corpus et le PDF source ne peuvent pas être choisis comme destination.

Le premier script conserve son rôle d'aperçu : au plus 2 000 caractères par page.
Le second reste spécifique à la structure du règlement 2019/2152 ; `--input` permet
notamment d'en traiter une copie située hors du dépôt et ne généralise pas le parseur
aux autres documents.

Les tests ciblés des entrées/sorties génèrent un petit PDF temporaire et ne nécessitent
aucun document du corpus :

```bash
python -m unittest discover -s tests -p test_extraction_io.py -v
```

## Licence

Le code et la documentation propres à ce dépôt sont publiés sous licence MIT. Les documents tiers référencés dans le catalogue restent soumis à leurs propres droits.
