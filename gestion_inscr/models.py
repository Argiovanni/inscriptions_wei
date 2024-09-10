# Create your models here.

from django.db import models
from django.utils import timezone


class Bungalow(models.Model):
    code = models.CharField(max_length=8, unique=True)
    nb_pers = models.IntegerField(default=0)
    caution_total = models.FloatField(default=0.0)
    
    def __str__(self) -> str:
        return self.code
    
    def get_members(self):
        return Inscrit.objects.filter(bungalow=self.id)
    
    def substract_from_caution(self, price):
        if price < 0:
            return
        
        if price > self.caution_total:
            self.caution_total = 0
        else:
            self.caution_total -= price
        
        if self.nb_pers > 0:
            members = self.get_members()
            for member in members:
                new_caution = member.valeur_caution - price/self.nb_pers
                if new_caution < 0:
                    print("/!\ problem new caution < 0")
                    member.update_caution(0)
                else:
                    member.update_caution(new_caution)
        self.save()
        return
    
    def add_pers(self, inscrit):
        self.nb_pers += 1
        self.caution_total += inscrit.valeur_caution
        inscrit.bungalow = self
        inscrit.save()
        self.save()
        return
    
    
                

class Inscrit(models.Model):
    PROMO_CHOICES = [("1A","1A"), ("2A","2A"), ("3A","3A"), ("V","vieux")]
    FILIERE_CHOICES = [("SN","SN"), ("3EA","3EA"), ("MF2E","MF2E"), ("AUX","Autres")]
    PAIEMENT_CHOICES = [('L', "Lydia"), ('C',"Chèque"), ('E', "Espèce")]
    BILLET_CHOICES = [('N',"non-cotisant"),('O',"Cotisant"), ('A',"AE"), ('C',"can7"), ('T',"tvn7"), ('P',"photo7")]

    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    promo = models.CharField(max_length=2, choices=PROMO_CHOICES, default="1A") # 1A / 2A / 3A / vieux
    filier = models.CharField(max_length=4, choices=FILIERE_CHOICES, default="SN") # SN / 3EA / MF2E
    cautisant = models.BooleanField(default=False)
    prix_place = models.FloatField(blank=True, null=True)
    paiement = models.CharField(max_length=1, default="L", choices=PAIEMENT_CHOICES) # lydia / chèque / espèce 
    place_paye = models.BooleanField(default=False)
    code_billet = models.CharField(max_length=16, unique=True, null=True) 
    caution = models.CharField(max_length=1, blank=True, choices=PAIEMENT_CHOICES)  # lydia / chèque / espèce
    caution_paye = models.BooleanField(default=False)
    valeur_caution = models.FloatField(default=100.0) # montant à rendre
    type_billet = models.CharField(max_length=1, default="N", choices=BILLET_CHOICES) # non_cautisant / cautisant / AE / CAN7 / TVN7 / PHOTO7 / Fanfare
    decharge_signe = models.BooleanField(default=False)
    date_paiement_place = models.DateTimeField(blank=True, null=True)
    date_paiement_caution = models.DateTimeField(blank=True, null=True)
    date_rendu_caution = models.DateTimeField(blank=True, null=True)
    bungalow = models.ForeignKey(Bungalow, on_delete=models.CASCADE, blank=True, null=True)
    staff_caisse_place = models.CharField(max_length=32, blank=True,null=True) # le staffeur qui encaisse à encaissé pendant la permanence
    staff_caisse_caution = models.CharField(max_length=32, blank=True,null=True) # le staffeur qui encaisse à encaissé pendant la permanence
    commentaires = models.CharField(max_length=255, blank=True, null=True) # si il y a un truc a signaler pendant l'inscription (e.g.: manque partie de la caution/décharge, modification par rapport au SG, etc)
    
    def __str__(self) -> str:
        return str(self.prenom) + " " + str(self.nom)
    
    def payer_place(self, mode, staffeur):
        self.paiement = mode
        self.place_paye = True
        self.date_paiement_place = timezone.now()
        self.staff_caisse_place = staffeur
        self.save()
        return
    
    def payer_caution(self, mode, staffeur):
        self.caution = mode
        self.caution_paye = True
        self.date_paiement_caution = timezone.now()
        self.staff_caisse_caution = staffeur
        self.save()
        return
    
    def update_caution(self, new_value):
        self.valeur_caution = new_value
        if (new_value == 0) :
            self.date_rendu_caution = timezone.now()
        self.save()
        return
    
    def rendre_caution(self):
        return self.update_caution(0)
    
    def update_decharge(self):
        self.decharge_signe = not self.decharge_signe
        self.save()
        return
    

