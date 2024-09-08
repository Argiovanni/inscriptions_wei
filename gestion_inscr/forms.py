from django import forms
from .models import Inscrit,Bungalow

PAIEMENT_CHOICES = [('L', "Lydia"), ('C',"Chèque"), ('E', "Espèce")]

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Identifiant",
                "class": "form-control"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "form-control"
        }))

class PaiementPlaceForm(forms.ModelForm):
    class Meta:
        model = Inscrit
        fields = ('paiement',)
    def __init__(self,  *args, **kwargs):
        super(PaiementPlaceForm, self).__init__(*args, **kwargs)
        self.fields['paiement'].queryset = [choice[1] for choice in PAIEMENT_CHOICES]
        
class PaiementCautionForm(forms.ModelForm):
    class Meta:
        model = Inscrit
        fields = ('caution',)
    def __init__(self,  *args, **kwargs):
        super(PaiementCautionForm, self).__init__(*args, **kwargs)
        self.fields['caution'].queryset = [choice[1] for choice in PAIEMENT_CHOICES]
        self.fields['caution'].empty_label = None
        
class AddMemberForm(forms.Form):
    participant = forms.ModelChoiceField(queryset=Inscrit.objects.filter(bungalow=None, place_paye=True, caution_paye=True), required=True)

class MontantCautionForm(forms.Form):
    montant = forms.FloatField(widget=forms.NumberInput,required=True, initial=0)


class CsvFileForm(forms.Form):
    csv_file = forms.FileField(
        required=False, 
        widget=forms.FileInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Upload "products.csv"', 
                'help_text': 'Choose a .csv file with products to enter'
        }))