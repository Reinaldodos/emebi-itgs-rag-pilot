# Provenance et droits des sources

## Principe

Le dépôt référence des documents institutionnels accessibles en ligne sans les
redistribuer. L'accès public ou gratuit ne constitue pas, à lui seul, une
autorisation de reproduction, de redistribution ou de publication dans un POC.
La licence MIT du dépôt couvre uniquement le code et la documentation produits
pour ce projet.

## Traçabilité par document

Le manifeste `metadata/catalogue.csv`, répliqué dans `catalogue.json`, conserve :

- `organisme`, qui identifie le producteur ou l'autorité responsable ;
- `url_source`, URL institutionnelle canonique utilisée pour qualifier le document ;
- `url_telechargement`, URL effective du fichier ou de la page collectée ;
- `date_consultation`, date à laquelle la ressource a été récupérée ;
- `date_version` et `date_publication`, laissées vides lorsqu'elles ne sont pas établies ;
- `sha256`, empreinte du fichier effectivement contrôlé ;
- `licence_ou_conditions`, preuve ou réserve connue concernant la réutilisation ;
- `statut_redistribution`, décision opérationnelle décrite ci-dessous.

L'URL de téléchargement peut changer sans que l'autorité ou la version du
document change. Inversement, un nom de fichier ou un millésime dans une URL ne
prouve pas une version : les dates ne sont renseignées que lorsqu'elles sont
établies dans la source.

## Statuts de redistribution

Le champ `statut_redistribution` utilise un vocabulaire fermé :

- `autorisee_sous_conditions` : une autorisation explicite a été identifiée ;
  les obligations et éventuelles exceptions restent décrites dans
  `licence_ou_conditions` ;
- `non_autorisee_sans_permission` : les conditions identifiées réservent les
  droits ; le document ne doit pas être redistribué sans autorisation distincte ;
- `a_verifier` : aucune preuve suffisante n'a été établie ; par défaut, le
  document reste local et n'est pas redistribué.

Ces statuts portent sur la redistribution des documents sources, pas sur leur
pertinence réglementaire ni sur la possibilité technique de les indexer
localement. Toute publication d'un POC doit réexaminer les conditions applicables,
en particulier les droits de tiers, les photographies et les extraits.

## Règle de publication

Seuls les URL, métadonnées, empreintes et éléments reproductibles propres au
projet sont versionnés. Les PDF, pages HTML, feuilles de calcul et archives
téléchargés restent exclus de Git. Un statut `autorisee_sous_conditions` ne vaut
pas décision automatique de publier le fichier : les conditions indiquées
doivent d'abord être appliquées et vérifiées.
