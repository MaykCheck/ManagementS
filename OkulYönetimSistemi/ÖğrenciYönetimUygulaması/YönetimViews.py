from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ÖğrenciEklemeForm, ÖğrenciGüncellemeForm
from .models import CustomUser, Çalışanlar, Dersler, Konular, Öğrenciler, SessionYılModel, ÖğrenciGeriBildirimi, ÇalışanGeriBildirimi, ÖğrenciİzinRaporu, ÇalışanİzinRaporu, Katılım, KatılımRaporu

def adminAnasayfa(request):
    bütünÖğrenciSayısı = Öğrenciler.objects.all().count()
    konuSayısı = Konular.objects.all().count()
    dersSayısı = Dersler.objects.all().count()
    çalışanSayısı = Çalışanlar.objects.all().count()
    bütünDersler = Dersler.objects.all()
    dersİsimListesi = []
    konuSayısıListesi = []
    derstekiÖğrenciSayısıListesi = []

    for ders in bütünDersler:
        konular = Konular.objects.filter(ders_id=ders.id).count()
        öğrenciler = Öğrenciler.objects.filter(ders_id=ders.id).count()
        dersİsimListesi.append(ders.dersAdı)
        konuSayısıListesi.append(konular)
        derstekiÖğrenciSayısıListesi.append(öğrenciler)

    bütünKonular = Konular.objects.all()
    konuListesi = []
    konudakiÖğrenciSayısıListesi = []
    for konu in bütünKonular:
        ders = Dersler.objects.get(id=konu.ders_id.id)
        öğrenciSayısı = Öğrenciler.objects.filter(ders_id=ders.id).count()
        konuListesi.append(konu.konuAdı)
        konudakiÖğrenciSayısıListesi.append(öğrenciSayısı)

    #çalışanlar için liste mantığı

    mevcutÇalışanYoklamaListesi = []
    çalışanYoklamaİzinListesi = []
    çalışanİsimListesi = []

    çalışanlar = Çalışanlar.objects.all()
    for çalışan in çalışanlar:
        konu_ids = Konular.objects.filter(çalışan_id = çalışan.admin.id)
        yoklama = Katılım.objects.filter(konu_id__in=konu_ids).count()
        izinler = ÇalışanİzinRaporu.objects.filter(çalışan_id=çalışan.id, izin_status=1).count()
        mevcutÇalışanYoklamaListesi.append(yoklama)
        çalışanYoklamaİzinListesi.append(izinler)
        çalışanİsimListesi.append(çalışan.admin.ad)

    #öğrenciler için liste mantığı

    mevcutÖğrenciYoklamaListesi = []
    öğrenciYoklamaİzinListesi = []
    öğrenciİsimListesi = []

    öğrenciler = Öğrenciler.objects.all()
    for öğrenci in öğrenciler:
        yoklama = KatılımRaporu.objects.filter(öğrenci_id=öğrenci.id, status=True).count()
        yok = KatılımRaporu.objects.filter(öğrenci_id=öğrenci.id, status=False).count()
        izinler = ÖğrenciİzinRaporu.objects.filter(öğrenci_id=öğrenci.id, izin_status=1).count()
        mevcutÖğrenciYoklamaListesi.append(yoklama)
        öğrenciYoklamaİzinListesi.append(izinler+yok)
        öğrenciİsimListesi(öğrenci.admin.ad)

    context={
        "bütünÖğrenciSayısı":bütünÖğrenciSayısı,
        "konuSayısı":konuSayısı,
        "dersSayısı":dersSayısı,
        "çalışanSayısı":çalışanSayısı,
        "dersİsimListesi":dersİsimListesi,
        "konuSayısıListesi":konuSayısıListesi,
        "derstekiÖğrenciSayısıListesi":derstekiÖğrenciSayısıListesi,
        "konuListesi":konuListesi,
        "konudakiÖğrenciSayısıListesi":konudakiÖğrenciSayısıListesi,
        "mevcutÇalışanYoklamaListesi":mevcutÇalışanYoklamaListesi,
        "çalışanYoklamaİzinListesi":çalışanYoklamaİzinListesi,
        "çalışanİsimListesi":çalışanİsimListesi,
        "mevcutÖğrenciYoklamaListesi":mevcutÖğrenciYoklamaListesi,
        "öğrenciYoklamaİzinListesi":öğrenciYoklamaİzinListesi,
        "öğrenciİsimListesi":öğrenciİsimListesi,
    }
    return render(request, "YönetimTemplate/anasayfaİçerik.html",context)

def çalışanEkle(request):
    return render(request, "YönetimTemplate/çalışanEkleTemplate.html")

def çalışanEkleKaydı(request):
    if request.method != "POST":
        messages.error(request, "Yanlış Method")
        return redirect('çalışanEkle')
    else:
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        kullanıcıAdı = request.POST.get('kullanıcıAdı')
        email = request.POST.get('email')
        şifre = request.POST.get('şifre')
        adres = request.POST.get('adres')

        try:
            user = CustomUser.objects.create_user(kullanıcıAdı=kullanıcıAdı,
                                                  şifre=şifre,
                                                  email=email,
                                                  ad=ad,
                                                  soyad=soyad,
                                                  user_type=2)
            user.çalışanlar.adres = adres #burada bir hata gözüküyor dikkat et!
            user.save()
            messages.success(request, "Çalışan Başarıyla Eklendi!")
            return redirect('çalışanEkle')
        except:
            messages.error(request, "Çalışan Eklenirken Bir Hata Oluştu!")
            return redirect('çalışanEkle')
        
def çalışanYönetimi(request):
    çalışanlar = Çalışanlar.objects.all()
    context = {
        "çalışanlar":çalışanlar
    }
    return render(request, "YönetimTemplate/çalışanYönetimiTemplate.html", context)

def çalışanGüncelleme(request, çalışan_id):
    çalışan = Çalışanlar.objects.get(admin=çalışan_id)

    context = {
        "çalışan":çalışan,
        "id":çalışan_id
    }
    return render(request, "YönetimTemplate/çalışanGüncellemeTemplate.html", context)

def çalışanGüncellemeKaydı(request):
    if request.method != "POST":
        return HttpResponse("<h2>İzinsiz Deneme!</h2>")
    else:
        çalışan_id = request.POST.get('çalışan_id')
        kullanıcıAdı = request.POST.get('kullanıcıAdı')
        email = request.POST.get('email')
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        adres = request.POST.get('adres')

        try:
            user = CustomUser.objects.get(id=çalışan_id)
            user.first_name = ad
            user.last_name = soyad
            user.email = email
            user.username = kullanıcıAdı
            user.save()

            çalışan_model = Çalışanlar.objects.get(admin=çalışan_id)
            çalışan_model.adres = adres
            çalışan_model.save()

            messages.success(request, "Çalışan Başarıyla Güncellendi.")
            return redirect('/çalışanGüncelleme/'+çalışan_id)
        except:
            messages.error(request,"Çalışan Güncellenirken Bir Hata Oluştu!")
            return redirect('/çalışanGüncelleme/'+çalışan_id)

def çalışanSilme(request, çalışan_id):
    çalışan = Çalışanlar.objects.get(admin=çalışan_id)
    try:
        çalışan.delete()
        messages.success(request, "Çalışan Başarıyla Silindi.")
        return redirect('çalışanYönetimi')
    except:
        messages.error(request, "Çalışan Silinirken Bir Hata Oluştu!")
        return redirect('çalışanYönetimi')
    
def dersEkleme(request):
    return render(request, "YönetimTemplate/dersEklemeTemplate.html")

def dersEklemeKaydı(request):
    if request.method != "POST":
        messages.error(request,"Yanlış Method!")
        return redirect('dersEkleme')
    else:
        ders = request.POST.get('ders')
        try:
            ders_model = Dersler(dersAdı = ders)
            ders_model.save()
            messages.success(request,"Ders Başarıyla Eklendi!")
            return redirect('dersEkleme')
        except:
            messages.error(request, "Ders Eklenirken Bir Hata Oluştu!")
            return redirect('dersEkleme')
        
def dersYönetimi(request):
    dersler = Dersler.objects.all()
    context = {
        'dersler':dersler
    }
    return render(request, 'YönetimTemplate/dersYönetimTemplate.html', context)

def dersGüncelleme(request, ders_id):
    ders = Dersler.objects.get(id=ders_id)
    context = {
        'ders':ders,
        'id':ders_id
    }
    return render(request, 'YönetimTemplate/dersGüncellemeTemplate.html', context)

def dersGüncellemeKaydı(request):
    if request.method != "POST":
        HttpResponse("Yanlış Method")
    else:
        ders_id = request.POST.get('ders_id')
        dersAdı = request.POST.get('ders')

        try:
            ders = Dersler.objects.get(id=ders_id)
            ders.dersAdı = dersAdı
            ders.save()
            messages.success(request, "Ders Başarıyla Güncellendi!")
            return redirect('/dersGüncelleme/'+ders_id)
        except:
            messages.error(request, "Ders Güncellenirken Bir Hata Oluştu!")
            return redirect('/dersGüncelleme/'+ders_id)
    
def dersSilme(request, ders_id):
    ders = Dersler.objects.get(id=ders_id)
    try:
        ders.delete()
        messages.success(request, "Ders Başarıyla Silindi.")
        return redirect('dersYönetimi')
    except:
        messages.error(request, "Ders Silinirken Bir Hata Oluştu!")
        return redirect('dersYönetimi')
    
def sessionYönetimi(request):
    sessionYılları = SessionYılModel.objects.all()
    context = {
        "sessionYılları":sessionYılları
    }
    return render(request, "YönetimTemplate/sessionYönetimiTemplate.html")

def sessionEkleme(request):
    return render(request, "YönetimTemplate/sessionEklemeTemplate.html")

def sessionEklemeKaydı(request):
    if request.method != "POST":
        messages.error(request,"Yanlış Method")
        return redirect('dersEkleme') #burasını böyle yazmış ama büyük ihtimalle sessionEkleme olacak
    else:
        sessionBaşlangıçYılı = request.POST.get('sessionBaşlangıçYılı')
        sessionBitişYılı = request.POST.get('sessionBitişYılı')
        try:
            sessionYılı = SessionYılModel(sessionBaşlangıçYılı=sessionBaşlangıçYılı,
                                          sessionBitişYılı=sessionBitişYılı)
            sessionYılı.save()
            messages.success(request, "Session Yılı Başarıyla Eklendi!")
            return redirect('sessionEkleme')
        except:
            messages.error(request, "Session Yılı Eklenirken Bir Hata Oluştu!")
            return redirect('sessionEkleme')
        
def sessionGüncelleme(request, session_id):
    sessionYılı = SessionYılModel.objects.get(id=session_id)
    context = {
        "sessionYılı":sessionYılı
    }
    return render(request, "YönetimTemplate/sessionGüncellemeTemplate.html", context)

def sessionGüncellemeKaydı(request):
    if request.method != "POST":
        messages.error(request, "Yanlış Method!")
        return redirect('sessionYönetimi')
    else:
        session_id = request.POST.get('session_id')
        sessionBaşlangıçYılı = request.POST.get('sessionBaşlangıçYılı')
        sessionBitişYılı = request.POST.get('sessionBitişYılı')
        try:
            sessionYılı = SessionYılModel.objects.get(id=session_id)
            sessionYılı.sessionBaşlangıçYılı = sessionBaşlangıçYılı
            sessionYılı.sessionBitişYılı = sessionBitişYılı
            sessionYılı.save()

            messages.success(request, "Session Yılı Başarıyla Güncellendi!")
            return redirect('/sessionGüncelleme/'+session_id)
        except:
            messages.error(request, "Session Yılı Güncellenirken Bir Hata Oluştu!")
            return redirect('/sessionGüncelleme/'+session_id)

def sessionSilme(request, session_id):
    session = SessionYılModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Sessio Başarıyla Silindi!")
        return redirect('sessionYönetimi')
    except:
        messages.error(request, "Session Silinirken Bir Hata Oluştu!")
        return redirect('sessionYönetimi')
    
def öğrenciEkleme(request):
    form = ÖğrenciEklemeForm()
    context = {
        "form":form
    }
    return render(request, 'YönetimTemplate/öğrenciEklemeTemplate.html', context)

def öğrenciEklemeKaydı(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('öğrenciEkleme')
    else:
        form = ÖğrenciEklemeForm(request.POST, request.FILES)
        
        if form.is_valid():
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            kullanıcıAdı = form.cleaned_data['kullanıcıAdı']
            email = form.cleaned_data['email']
            şifre = form.cleaned_data['şifre']
            adres = form.cleaned_data['adres']
            sessionYılı_id = form.cleaned_data['sessionYılı_id']
            ders_id = form.cleaned_data['ders_id']
            cinsiyet = form.cleaned_data['cinsiyet']

            if len(request.FILES) != 0:
                profilFotoğrafı = request.FILES['profilFotoğrafı']
                fs = FileSystemStorage()
                filename = fs.save(profilFotoğrafı.name, profilFotoğrafı) #mümkün bir bug konumu!!!
                profilFotoğrafı_url = fs.url(filename)
            else:
                profilFotoğrafı_url = None
            
            try:
                user = CustomUser.objects.create_user(kullanıcıAdı=kullanıcıAdı,
                                                      şifre=şifre,
                                                      email=email,
                                                      ad=ad,
                                                      soyad=soyad,
                                                      user_type=3)
                user.öğrenciler.adres = adres

                dersObj = Dersler.objects.get(id=ders_id)
                user.öğrenciler.ders_id = dersObj

                sessionYılObj = SessionYılModel.objects.get(id=sessionYılı_id)
                user.öğrenciler.sessionYılı_id = sessionYılObj

                user.öğrenciler.cinsiyet = cinsiyet
                user.öğrenciler.profilFotoğrafı = profilFotoğrafı_url
                user.save()
                messages.success(request, "Öğrenci Başarıyla Eklendi!")
                return redirect('öğrenciEkleme')
            except:
                messages.error(request, "Öğrenci Eklenirken Bir Hata Oluştu!")
                return redirect('öğrenciEkleme')
        else:
            return redirect('öğrenciEkleme')

def öğrenciYönetimi(request):
    öğrenciler = Öğrenciler.objects.all()
    context = {
        "öğrenciler":öğrenciler
    }
    return render(request, 'YönetimTemplate/öğrenciYönetimTemplate.html', context)

def öğrenciGüncelleme(request, öğrenci_id):
    request.session['öğrenci_id'] = öğrenci_id

    öğrenci = Öğrenciler.objects.get(admin=öğrenci_id)
    form = ÖğrenciGüncellemeForm()

    form.fields['email'].initial = öğrenci.admin.email
    form.fields['kullanıcıAdı'].initial = öğrenci.admin.username
    form.fields['ad'].initial = öğrenci.admin.first_name
    form.fields['soyad'].initial = öğrenci.admin.last_name
    form.fields['adres'].initial = öğrenci.adres
    form.fields['ders_id'].initial = öğrenci.ders_id.id
    form.fields['cinsiyet'].initial = öğrenci.cinsiyet
    form.fields['sessionYılı_id'] = öğrenci.sessionYılı_id.id

    context = {
        "id":öğrenci_id,
        "kullanıcıAdı":öğrenci.admin.username,
        "form":form
    }
    return render(request, "YönetimTemplate/öğrenciGüncellemeTemplate.html", context)

def öğrenciGüncellemeKaydı(request):
    if request.method != "POST":
        return HttpResponse("Yanlış Method!")
    else:
        öğrenci_id = request.session.get('öğrenci_id')
        if öğrenci_id == None:
            return redirect('/öğrenciYönetimi')
 
        form = ÖğrenciGüncellemeForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            kullanıcıAdı = form.cleaned_data['kullanıcıAdı']
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            adres = form.cleaned_data['adres']
            ders_id = form.cleaned_data['ders_id']
            cinsiyet = form.cleaned_data['cinsiyet']
            sessionYılı_id = form.cleaned_data['sessionYılı_id']

            if len(request.FILES) != 0:
                profilFotoğrafı = request.FILES['profilFotoğrafı']
                fs = FileSystemStorage()
                filename = fs.save(profilFotoğrafı.name, profilFotoğrafı)
                profilFotoğrafı_url = fs.url(filename)
            else:
                profilFotoğrafı_url = None
 
            try:
                user = CustomUser.objects.get(id=öğrenci_id)
                user.first_name = ad
                user.last_name = soyad
                user.email = email
                user.username = kullanıcıAdı
                user.save()
 
                öğrenciModel = Öğrenciler.objects.get(admin=öğrenci_id)
                öğrenciModel.adres = adres
 
                ders = Dersler.objects.get(id=ders_id)
                öğrenciModel.ders_id = ders
 
                SessionYılıObj = SessionYılModel.objects.get(id=sessionYılı_id)
                öğrenciModel.sessionYılı_id = SessionYılıObj

                öğrenciModel.cinsiyet = cinsiyet
                if profilFotoğrafı_url != None:
                    öğrenciModel.profilFotoğrafı = profilFotoğrafı_url
                öğrenciModel.save()
                del request.session['öğrenci_id']

                messages.success(request, "Öğrenci Başarıyla Güncellendi!")
                return redirect('/öğrenciGüncelleme/'+öğrenci_id)
            except:
                messages.success(request, "Öğrenci Güncellenirken Bir Hata Oluştu!")
                return redirect('/öğrenciGüncelleme/'+öğrenci_id)
        else:
            return redirect('/öğrenciGüncelleme/'+öğrenci_id)

def öğrenciSilme(request, öğrenci_id):
    öğrenci = Öğrenciler.objects.get(admin=öğrenci_id)
    try:
        öğrenci.delete()
        messages.success(request, "Öğrenci Başarıyla Silindi!")
        return redirect('öğrenciYönetimi')
    except:
        messages.error(request, "Öğrenci Silinirken Bir Hata Oluştu!")
        return redirect('öğrenciYönetimi')
    
def konuEkleme(request):
    dersler = Dersler.objects.all()
    çalışanlar = CustomUser.objects.filter(user_type='2')
    context = {
        "dersler":dersler,
        "çalışanlar":çalışanlar,
    }
    return render(request, 'YönetimTemplate/konuEklemeTemplate.html', context)

def konuEklemeKaydı(request):
    if request.method != "POST":
        messages.error(request,"İzinsiz Method!")
        return redirect('konuEkleme')
    else:
        konuAdı = request.POST.get('konu')

        ders_id = request.POST.get('ders')
        ders = Dersler.objects.get(id=ders_id)

        çalışan_id = request.POST.get('çalışan')
        çalışan = CustomUser.objects.get(id=çalışan_id)

        try:
            konu = Konular(konuAdı = konuAdı,
                           ders_id = ders,
                           çalışan_id = çalışan)
            konu.save()
            messages.success(request, "Konu Başarıyla Eklendi!")
            return redirect('konuEkleme')
        except:
            messages.error(request, 'Konu Eklenirken Hata Oluştu!')
            return redirect('konuEkleme')
        
def konuYönetimi(request):
    konular = Konular.objects.all()
    context = {
        "konular":konular
    }
    return render(request, 'YönetimTemplate/konuYönetimiTemplate.html', context)

def konuGüncelleme(request, konu_id):
    konu = Konular.objects.get(id=konu_id)
    dersler = Dersler.objects.all()
    çalışanlar = CustomUser.objects.filter(user_type='2')
    context = {
        "konu":konu,
        "dersler":dersler,
        "çalışanlar":çalışanlar,
        "id":konu_id
    }
    return render(request, 'YönetimTemplate/konuGüncellemeTemplate.html', context)

def konuGüncellemeKaydı(request):
    if request.method != "POST":
        HttpResponse('Yanlış Method.')
    else:
        konu_id = request.POST.get('konu_id')
        konuAdı = request.POST.get('konu')
        ders_id = request.POST.get('ders')
        çalışan_id = request.POST.get('çalışan')

        try:
            konu = Konular.objects.get(id=konu_id)
            konu.konuAdı = konuAdı

            ders = Dersler.objects.get(id=ders_id)
            konu.ders_id = ders

            çalışan = CustomUser.objects.get(id=çalışan_id)
            konu.çalışan_id = çalışan

            konu.save()

            messages.success(request, "Konu Başarıyla Güncellendi!")
            return HttpResponseRedirect(reverse("konuGüncelleme",kwargs={"konu_id":konu_id}))
        except:
            messages.error(request, "Konu Güncellenirken Bir Hata Oluştu")
            return HttpResponseRedirect(reverse('konuGüncelleme',kwargs={"konu_id":konu_id}))
        
def konuSilme(request, konu_id):
    konu = Konular.objects.get(id=konu_id)
    try:
        konu.delete()
        messages.success(request,"Konu Başarıyla Silindi!")
        return redirect('konuYönetimi')
    except:
        messages.error(request, "Konu Silinirken Bir Hata Oluştu.")
        return redirect('konuYönetimi')
    
@csrf_exempt
def emailKontrol(request):
    email = request.POST.get("email")
    userObj = CustomUser.objects.filter(email=email).exists()
    if userObj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
@csrf_exempt
def kullanıcıAdıKontrol(request):
    kullanıcıAdı = request.POST.get('kullanıcıAdı')
    userObj = CustomUser.objects.filter(kullanıcıAdı=kullanıcıAdı).exists()
    if userObj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
def öğrenciGeriBildirimMesajı(request):
    geriBildirimler = ÖğrenciGeriBildirimi.objects.all()
    context = {
        "geriBildirimler":geriBildirimler
    }
    return render(request, 'YönetimTemplate/öğrenciGeriBildirimiTemplate.html', context)

@csrf_exempt
def öğrenciGeriBildirimMesajıCevabı(request):
    geriBildirim_id = request.POST.get('id')
    geriBildirimCevabı = request.POST.get('cevap')

    try:
        geriBildirim = ÖğrenciGeriBildirimi.objects.get(id=geriBildirim_id)
        geriBildirim.geriBildirimCevabı = geriBildirimCevabı
        geriBildirim.save()
        return HttpResponse('True')
    except:
        return HttpResponse('False')
    
def çalışanGeriBildirimMesajı(request):
    geriBildirimler = ÇalışanGeriBildirimi.objects.all()
    context = {
        "geriBildirimler":geriBildirimler
    }
    return render(request, 'YönetimTemplate/çalışanGeriBildirimiTemplate.html', context)

@csrf_exempt
def çalışanGeriBildirimMesajıCevabı(request):
    geriBildirim_id = request.POST.get('id')
    geriBildirimCevabı = request.POST.get('cevap')
    try:
        geriBildirim = ÇalışanGeriBildirimi.objects.get(id=geriBildirim_id)
        geriBildirim.geriBildirimCevabı = geriBildirimCevabı
        geriBildirim.save()
        return HttpResponse('True')
    except:
        return HttpResponse('False')
    
def öğrenciİzinView(request):
    izinler = ÖğrenciİzinRaporu.objects.all()
    context = {
        "izinler":izinler
    }
    return render(request, 'YönetimTemplate/öğrenciİzinView.html', context)

def öğrenciİzinOnay(request, izin_id):
    izin = ÖğrenciİzinRaporu.objects.get(id=izin_id)
    izin.izin_status = 1
    izin.save()
    return redirect('öğrenciİzinView')

def öğrenciİzinRed(request, izin_id):
    izin = ÖğrenciİzinRaporu.objects.get(id=izin_id)
    izin.izin_status = 2
    izin.save()
    return redirect('öğrenciİzinView')

def çalışanİzinView(request):
    izinler = ÇalışanİzinRaporu.objects.all()
    context = {
        'izinler':izinler
    }
    return render(request, 'YönetimTemplate/çalışanİzinView.html', context)

def çalışanİzinOnay(request, izin_id):
    izin = ÇalışanİzinRaporu.objects.get(id=izin_id)
    izin.izin_status = 1
    izin.save()
    return redirect('çalışanİzinView')

def çalışanİzinRed(request, izin_id):
    izin = ÇalışanİzinRaporu.objects.get(id=izin_id)
    izin.izin_status = 2
    izin.save()
    return redirect('çalışanİzinView')

def adminViewKatılım(request):
    konular = Konular.objects.all()
    sessionYılları = SessionYılModel.objects.all()
    context = {
        "konular":konular,
        "sessionYılları":sessionYılları
    }
    return render(request, "YönetimTemplate/adminViewKatılım.html", context)

@csrf_exempt
def adminGetKatılımTarihleri(request):
    
    konu_id = request.POST.get('konu')
    sessionYılı = request.POST.get('sessionYılı_id')

    konuModel = Konular.objects.get(id=konu_id)

    sessionModel = SessionYılModel.objects.get(id=sessionYılı)
    yoklama = Katılım.objects.filter(konu_id=konuModel,
                                     sessionYılı_id=sessionModel)
    
    list_data = []
    
    for tekliYoklama in yoklama:
        data_small = {"id":tekliYoklama.id,
                      "yoklamaTarihi":str(tekliYoklama.yoklamaTarihi),
                      "sessionYılı_id":tekliYoklama.sessionYılı_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),
                        content_type = "application/json",
                        safe=False)

@csrf_exempt
def adminGetÖğrenciKatılım(request):

    yoklamaTarihi = request.POST.get('yoklamaTarihi')
    yoklama = Katılım.objects.get(id=yoklamaTarihi)

    yoklamaData = KatılımRaporu.objects.filter(yoklama_id=yoklama)
    
    list_data = []

    for öğrenci in yoklamaData:
        data_small={"id":öğrenci.öğrenci_id.admin.id,
                    "name":öğrenci.öğrenci_id.admin.first_name+" "+öğrenci.öğrenci_id.admin.last_name,
                    "status":öğrenci.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),content_type='application/json', safe=False)

def adminProfili(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user":user
    }
    return render(request,'YönetimTemplate/adminProfili.html', context)

def adminProfilGüncelleme(request):
    if request.method != "POST":
        messages.error(request, "Yanlış Method!")
        return redirect('adminProfili')
    else:
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        şifre = request.POST.get('şifre')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = ad
            customuser.last_name = soyad
            if şifre != None and şifre != "":
                customuser.set_password(şifre)
            customuser.save()
            messages.success(request, "Profil Başarıyla Güncellendi!")
            return redirect('adminProfili')
        except:
            messages.error(request, "Profil Güncellenirken Bir Sorun Yaşandı")
            return redirect('adminProfili')
        
def çalışanProfili(request):
    pass

def öğrenciProfili(request):
    pass