"""Completer le journal des essais UI observes (heure exacte non conservee)."""
import csv
from collect_corpus import ROOT,LOGFIELDS,NOW

events=[
 ('D11','https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000888573/2026-10-06','recu_apres_timeout','Timeout interface 20 s; fichier HTML effectivement arrive et valide lors de l import'),
 ('D12','https://www.legifrance.gouv.fr/download/pdf?id=0HBNfiPl0shPIt5EdufogPJM530GUFJ9awgXQ4O_4Uw=','echec','Timeout navigateur 15 s, aucun fichier local retrouve'),
 ('D16','https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:02020R1197-20260305','echec','Timeout navigateur 20 s, repli Office des publications reussi ensuite'),
 ('D17','https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:02021R1704-20260510','echec','Timeout navigateur 15 s, aucun fichier local retrouve'),
 ('D18','https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=OJ:L_202600047','echec','Timeout navigateur 15 s, aucun fichier local retrouve'),
 ('D34','https://www.legifrance.gouv.fr/download/pdf?id=QsPi44J2BiKdxWSq9iK5I2KprXcSf2MrYdYfS2fg9qk=','echec','Timeout navigateur 15 s, aucun fichier local retrouve'),
 ('D35','https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006191662/2026-10-06','echec','Timeout navigateur 15 s, aucun fichier local retrouve'),
 ('D37','https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX:32004R0638','echec','Navigation navigateur timeout 10 s; recuperation Cellar reussie ensuite'),
 ('D38','https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX:02009R0471-20161223','echec','Commande navigateur focus timeout 10 s'),
]


def main() -> None:
    """Ajouter les essais au journal seulement lors d'un appel explicite."""
    path=ROOT/'logs/telechargements.csv'
    with path.open(encoding='utf-8',newline='') as f:
        existing={(r['id'],r['url'],r['methode']) for r in csv.DictReader(f)}
    with path.open('a',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=LOGFIELDS)
        for key,url,result,error in events:
            if (key,url,'navigateur_ordinaire_audit') in existing:continue
            w.writerow(dict(horodatage=NOW,id=key,passe=3,methode='navigateur_ordinaire_audit',url=url,url_finale='',http='',resultat=result,erreur=error+'; audit a posteriori, heure exacte non conservee',octets='',duree_secondes=''))
    print('Essais navigateur ajoutes au journal sans duplications.')


if __name__ == "__main__":
    main()
