### ce script ajoute a la DB les inscrit depuis un fichier .csv
from django.core.management.base import BaseCommand, CommandParser
import csv
from datetime import datetime
from gestion_inscr.models import Inscrit

class Command(BaseCommand):
    
    help = 'populate DB using csv file passed in param'
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('csv_file_path', type=str, help="path to the csv")
    
    def handle(self,*args, **kwargs):
        # now do the things that you want with your models here
        csv_file_path = kwargs['csv_file_path']
        print("start script")
        with open(csv_file_path, 'r') as fd :
            reader = csv.reader(fd,  delimiter=';')
            next(reader, None) # skip header
            nb_created = 0
            for row in reader:
                nom_prenom = row[1].split()
                prenom = nom_prenom[0]
                nom = ' '.join(nom_prenom[1:])
                if not nom.strip():
                    nom = "------"
                
                if row[3] == "Oui":
                    place_paye = True
                    
                else :
                    place_paye = False
                
                type_paiement = row[7]
                if type_paiement == "Lydia" :
                    paiement = 'L'
                elif type_paiement == "Cash" :
                    paiement = 'E'
                else : # chèque
                    paiement = 'C'
                
                type_billet = row[8]
                if ("Non cotisants" in type_billet):
                    billet = 'N'
                else:
                    billet = 'O'

                if row[9] == "Oui":
                    cotise_AE = True
                else :
                    cotise_AE = False
                
                # should not be usefull but let it here for now
                if (billet == 'O') and not cotise_AE:
                    comment = "/!\ need payer cotisation"
                else :
                    comment = None
                
                filiere = row[10]
                if not filiere.strip():
                    filiere = "AUX"
                    
                promo = row[11]
                if not promo.strip():
                    promo = "V"
                
                if promo == "1A":
                    caution = 100.0
                else :
                    caution = 200.0
                
                # prix 
                prix = float(row[15])
                
                code_billet = row[13]
                
                try:
                    inscrit_obj = Inscrit.objects.get(code_billet=code_billet)
                except Inscrit.DoesNotExist:
                    inscrit_obj = None
                    
                if inscrit_obj:
                    # inscrit exist in DB
                    pass
                else:
                    if row[6] == "Oui":
                        # place annulée
                        pass
                    else:
                        inscrit_obj = Inscrit.objects.create(nom=nom,prenom=prenom,promo=promo,filier=filiere,
                                    cautisant=cotise_AE, prix_place=prix,paiement=paiement,place_paye=place_paye,
                                    code_billet=code_billet,valeur_caution= caution, type_billet=billet, commentaires=comment)
                        nb_created += 1
                        print("created inscrit : ", inscrit_obj)
            print("nb inscrit objects created : ", nb_created)
                