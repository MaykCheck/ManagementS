from django import forms
from .models import Dersler, SessionYılModel

class DateInput(forms.DateInput):
    input_type = "date"

class ÖğrenciEklemeForm(forms.Form):
    email = forms.EmailField(label='Email',
                             max_length=50,
                             widget = forms.EmailInput(attrs={"class":"form-control"}))
    şifre = forms.CharField(label="Şifre",
                            max_length=50,
                            widget=forms.PasswordInput(attrs={"class":"form-control"}))
    ad = forms.CharField(label="Ad",
                         max_length=50,
                         widget=forms.TextInput(attrs={"class":"form-control"}))
    soyad = forms.CharField(label="Soyad",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    kullanıcıAdı = forms.CharField(label="Kullanıcı Adı",
                                   max_length=50,
                                   widget=forms.TextInput(attrs={"class":"form-control"}))
    adres = forms.CharField(label="Adres",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    
    try:
        dersler = Dersler.objects.all()
        dersListesi = []
        for ders in dersler:
            tekDers = (ders.id, ders.dersAdı)
            dersListesi.append(tekDers)
    except:
        print("here")
        dersListesi = []
    
    try:
        sessionYılları = SessionYılModel.objects.all()
        sessionYılıListesi = []
        for sessionYılı in sessionYılları:
            tekSessionYılı = (sessionYılı.id, str(sessionYılı.sessionBaşlangıçYılı)+" to "+str(sessionYılı.sessionBitişYılı))
            sessionYılıListesi.append(tekSessionYılı)
    except:
        sessionYılıListesi = []

    cinsiyetListesi = (
        ('Erkek','Erkek'),
        ('Kadın','Kadın')
    )
    ders_id = forms.ChoiceField(label="Ders",
                                choices=dersListesi,
                                widget=forms.Select(attrs={"class":"form-control"}))
    cinsiyet = forms.ChoiceField(label="Cinsiyet",
                                 choices=cinsiyetListesi,
                                 widget=forms.Select(attrs={"class":"form-control"}))
    sessionYılı_id = forms.ChoiceField(label="Session Yılı",
                                       choices=sessionYılıListesi,
                                       widget=forms.Select(attrs={"class":"form-control"}))
    profilFotoğrafı = forms.FileField(label="Profil Fotoğrafı",
                                      required=False,
                                      widget=forms.FileInput(attrs={"class":"form-control"}))

class ÖğrenciGüncellemeForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class":"form-control"}))
    ad = forms.CharField(label="Ad",
                         max_length=50,
                         widget=forms.TextInput(attrs={"class":"form-control"}))
    soyad = forms.CharField(label="Soyad",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    kullanıcıAdı = forms.CharField(label="Kullanıcı Adı",
                                   max_length=50,
                                   widget=forms.TextInput(attrs={"class":"form-control"}))
    adres = forms.CharField(label="Adres",
                            max_length=50,
                            widget=forms.TextInput(attrs={"class":"form-control"}))
    
    try:
        dersler = Dersler.objects.all()
        dersListesi = []
        for ders in dersler:
            tekDers = (ders.id, ders.dersAdı)
            dersListesi.append(tekDers)
    except:
        dersListesi = []

    try:
        sessionYılları = SessionYılModel.objects.all()
        sessionYılıListesi = []
        for sessionYılı in sessionYılları:
            tekSessionYılı = (sessionYılı.id, str(sessionYılı.sessionBaşlangıçYılı)+" to "+str(sessionYılı.sessionBitişYılı))
            sessionYılıListesi.append(tekSessionYılı)
    except:
        sessionYılıListesi = []

    cinsiyetListesi = (
        ('Erkek','Erkek'),
        ('Kadın','Kadın')
    )

    ders_id = forms.ChoiceField(label="Ders",
                                choices=dersListesi,
                                widget=forms.Select(attrs={"class":"form-control"}))
    cinsiyet = forms.ChoiceField(label="Cinsiyet",
                                 choices=cinsiyetListesi,
                                 widget=forms.Select(attrs={"class":"form-control"}))
    sessionYılı_id = forms.ChoiceField(label="Session Yılı",
                                       choices=sessionYılıListesi,
                                       widget=forms.Select(attrs={"class":"form-control"}))
    profilFotoğrafı = forms.FileField(label="Profil Fotoğrafı",
                                      required=False,
                                      widget=forms.FileInput(attrs={"class":"form-control"}))