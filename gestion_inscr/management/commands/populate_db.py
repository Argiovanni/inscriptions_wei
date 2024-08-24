### ce script ajoute a la DB les inscrit depuis un fichier .csv
from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from gestion_inscr.models import Inscrit

class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here
        csv_file_path = 'csv_sg_churros/ShotgunWEI2023.csv' # Replace with your actual file path
        print("start script")
        with open(csv_file_path, 'r') as fd :
            reader = csv.reader(fd)
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
                elif type_paiement == "Check" :
                    paiement = 'C'
                else :
                    paiement = ''
                    print("pb row 7 : methode paiement non reconu", type_paiement)
                
                type_billet = row[8]
                if (type_billet == "cotisants"):
                    billet = 'O'
                else:
                    billet = type_billet[0].upper()
                    if billet == 'F':
                        billet = 'A'

                if row[9] == "Oui":
                    cotise_AE = True
                else :
                    cotise_AE = False
                
                if (type_billet != "non cotisants") and not cotise_AE:
                    comment = "/!\ need payer cotisation"
                else :
                    comment = None
                
                filiere = row[10]
                if not filiere.strip():
                    filiere = "AUX"
                    
                promo = row[11]
                if not promo.strip():
                    promo = "V"
                
                # prix 
                #  BILLET_CHOICES = [('N',"non-cotisant"),('O',"Cotisant"), ('A',"AE"), ('C',"can7"), ('T',"tvn7"), ('P',"photo7")]
                if billet == 'C': #Can7
                    prix = 0.0
                elif billet == 'O': #cautisant
                    if promo == "1A":
                        prix = 140.0 # a voir si c'est le bon prix
                    else :
                        prix = 160.0 # a voir si c'est le bon prix
                elif billet == 'N': #non cautisant
                    prix = 205.0 # a voir si c'est le bon prix
                else: # AE, tvn7, photo7, 
                    prix = 145.0
                
                code_billet = row[13]
                
                try:
                    inscrit_obj = Inscrit.objects.get(code_billet=code_billet)
                except Inscrit.DoesNotExist:
                    inscrit_obj = None
                    
                if inscrit_obj:
                    # inscrit exist in DB
                    pass
                else:
                    inscrit_obj = Inscrit.objects.create(nom=nom,prenom=prenom,promo=promo,filier=filiere,
                                cautisant=cotise_AE, prix_place=145.0,paiement=paiement,place_paye=place_paye,
                                code_billet=code_billet,type_billet=billet, commentaires=comment)
                    nb_created += 1
                    print("created inscrit : ", inscrit_obj)
            print("nb inscrit objects created : ", nb_created)
                