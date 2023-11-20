from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import CustomUser, Çalışanlar, Dersler, Konular, Öğrenciler, SessionYılModel, Katılım, KatılımRaporu, ÇalışanİzinRaporu, ÇalışanGeriBildirimi, ÖğrenciSonuçları 

def çalışanAnasayfa(request):
    print(request.user.id)
    konular = Konular.objects.filter(çalışan_id=request.user.id)
    print(konular)
    ders_id_list = []
    for konu in konular:
        ders = Dersler.objects.get(id=konu.ders_id.id)
        ders_id_list.append(ders.id)

    finalDers = []
    for ders_id in ders_id_list:
        if ders_id  not in finalDers:
            finalDers.append(ders_id)

    print(finalDers)
    öğrenciSayısı = Öğrenciler.objects.filter(ders_id__in=finalDers).count()
    konuSayısı = konu.count()
    print(konuSayısı)
    print(öğrenciSayısı)

    katılımSayısı = Katılım.objects.filter(konu_id__in=konular).count()

    print(request.user.user_type)
    çalışan = Çalışanlar.objects.get(admin=request.user.id)
    izinSayısı = ÇalışanİzinRaporu.objects.filter(çalışan_id=çalışan.id,
                                                  izin_status=1).count()
    
    konuListesi = []
    katılımListesi = []
    for konu in konular:
        katılımSayısı1 = Katılım.objects.filter(konu_id=konu.id).count()
        konuListesi.append(konu.konuAdı)
        katılımListesi.append(katılımSayısı1)

    öğrenciKatılımı = Öğrenciler.objects.filter(ders_id__in=finalDers)
    öğrenciListesi = []
    öğrenciMevcutKatılımListesi = []
    öğrenciEksikListesi = []
    for öğrenci in öğrenciKatılımı:
        mevcutKatılımSayısı = KatılımRaporu.objects.filter(status=True,
                                                          öğrenci_id=öğrenci.id)
        eksikKatılımSayısı = KatılımRaporu.objects.filter(status=False,
                                                          öğrenci_id=öğrenci.id)
        öğrenciListesi.append(öğrenci.admin.ad+" "+öğrenci.admin.soyad)
        öğrenciMevcutKatılımListesi.append(mevcutKatılımSayısı)
        öğrenciEksikListesi.append(eksikKatılımSayısı)

    context={
        "öğrenciSayısı":öğrenciSayısı,
        "katılımSayısı":katılımSayısı,
        "izinSayısı":izinSayısı,
        "konuSayısı":konuSayısı,
        "konuListesi":konuListesi,
        "katılımListesi":katılımListesi,
        "öğrenciListesi":öğrenciListesi,
        "mevcutKatılımListesi":öğrenciMevcutKatılımListesi,
        "eksikKatılımListesi":öğrenciEksikListesi
    }
    return render(request,"ÇalışanTemplate/çalışanAnasayfaTemplate.html",context)

def çalışanYoklamaAlımı(request):
    konular = Konular.objects.filter(çalışan_id=request.user.id)
    sessionYılı = SessionYılModel.objects.all()
    context = {
        "konular":konular,
        "sessionYılı":sessionYılı
    }
    return render(request, "ÇalışanTemplate/yoklamaAlımıTemplate.html",context)

def çalışanİzinTalebi(request):
    çalışanObj = Çalışanlar.objects.get(admin=request.user.id)
    izinData = ÇalışanİzinRaporu.objects.filter(çalışan_id=çalışanObj)
    context = {
        "izinData":izinData
    }
    return render(request,"ÇalışanTemplate/çalışanİzinTalebi.html",context)

def çalışanİzinTalebiKaydı(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method")
        return redirect('çalışanİzinTalebi')
    else:
        izinTarihi = request.POST.get('izinTarihi')
        izinMesajı = request.POST.get('izinMesajı')

        çalışanObj = Çalışanlar.objects.get(admin=request.user.id)
        try:
            izinRaporu = ÇalışanİzinRaporu(çalışan_id=çalışanObj,
                                           izinTarihi=izinTarihi,
                                           izinMesajı=izinMesajı,
                                           izin_status=0)
            izinRaporu.save()
            messages.success(request,"Applied for Leave.")
            return redirect('çalışanİzinTalebi')
        except:
            messages.error(request,"Failed to Apply Leave")
            return redirect('çalışanİzinTalebi')
        
def çalışanGeriBildirimi(request):
    return render(request, "ÇalışanTemplate/çalışanGeriBildirimiTemplate.html")

def çalışanGeriBildirimiKaydı(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method.")
        return redirect('ÇalışanGeriBildirimi')
    else:
        geriBildirim = request.POST.get('geriBildirimMesajı')
        çalışanObj = Çalışanlar.objects.get(admin=request.user.id)

        try:
            geriBildirimEkle = ÇalışanGeriBildirimi(çalışan_id=çalışanObj,
                                                    geriBildirim=geriBildirim,
                                                    geriBildirimCevabı="")
            geriBildirimEkle.save()
            messages.success(request,"Feedback Sent.")
            return redirect('çalışanGeriBildirimi')
        except:
            messages.error(request,"Failed to Send Feedback.")
            return redirect('çalışaGeriBildirimi')

@csrf_exempt
def getÖğrenciler(request):
    konu_id = request.POST.get("konu")
    sessionYılı = request.POST.get("sessionYılı")

    konuModeli = Konular.objects.get(id=konu_id)
    sessionModeli = SessionYılModel.objects.get(id=sessionYılı)
    öğrenciler = Öğrenciler.objects.filter(ders_id=konuModeli.ders_id,
                                           sessionYılı_id=sessionModeli)
    listData = []

    for öğrenci in öğrenciler:
        data_small={"id":öğrenci.admin.id,
                    "ad":öğrenci.admin.ad+" "+öğrenci.admin.soyad}
        listData.append(data_small)
    return JsonResponse(json.dumps(listData),content_type="application/json",safe=False)

@csrf_exempt
def yoklamaBilgisiKaydı(request):
    öğrenci_ids = request.POST.get("öğrenci_ids")
    konu_id = request.POST.get("konu_id")
    yoklamaTarihi = request.POST.get("yoklamaTarihi")
    sessionYılı_id = request.POST.get("sessionYılı_id")

    konuModeli = Konular.objects.get(id=konu_id)
    sessionYılModel = SessionYılModel.objects.get(id=sessionYılı_id)

    jsonÖğrenci = json.loads(öğrenci_ids)

    try:
        yoklama = Katılım(konu_id=konuModeli,
                          yoklamaTarihi=yoklamaTarihi,
                          sessionYılı_id=sessionYılModel)
        yoklama.save()
        
        for öğre in jsonÖğrenci:
            öğrenci = Öğrenciler.objects.get(admin=öğre['id'])
            yoklamaRaporu = KatılımRaporu(öğrenci_id=öğrenci,
                                          yoklama_id=yoklama,
                                          status=öğre['status'])
            yoklamaRaporu.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
    
def çalışanYoklamaGüncelleme(request):
    konular = Konular.objects.filter(çalışan_id=request.user.id)
    sessionYılı = SessionYılModel.objects.all()
    context = {
        "konular":konular,
        "sessionYılı":sessionYılı
    }
    return render(request, "ÇalışanTemplate/yoklamaGüncelleme.html",context)

@csrf_exempt
def getYoklamaTarihleri(request):
    konu_id = request.POST.get("konu")
    sessionYılı = request.POST.get("sessionYılı_id")

    konuModeli = Konular.objects.get(id=konu_id)
    
    sessionModel = SessionYılModel.objects.get(id=sessionYılı)
    yoklama = Katılım.objects.filter(konu_id=konuModeli,
                                     sessionYılı_id=sessionModel)

    listData = []
     
    for yoklamaTekli in yoklama:
        data_small={"id":yoklamaTekli.id,
                    "yoklamaTarihi":str(yoklamaTekli.yoklamaTarihi),
                    "sessionYılı_id":yoklamaTekli.sessionYılı_id.id}
        listData.append(data_small)

    return JsonResponse(json.dumps(listData),
                        content_type="application/json",safe=False)

@csrf_exempt
def getÖğrenciYoklama(request):
    yoklamaTarihi = request.POST.get('yoklamaTarihi')
    yoklama = Katılım.objects.get(id=yoklamaTarihi)

    yoklamaData = KatılımRaporu.objects.filter(yoklama_id=yoklama)

    listData = []

    for öğrenci in yoklamaData:
        data_small={"id":öğrenci.öğrenci_id.admin.id,
                    "ad":öğrenci.öğrenci_id.admin.ad+" "+öğrenci.öğrenci_id.admin.soyad, "status":öğrenci.status}
        listData.append(data_small)
    
    return JsonResponse(json.dumps(listData),
                        content_type="application/json",
                        safe=False)

@csrf_exempt
def yoklamaBilgisiGüncelleme(request):
    öğrenci_ids = request.POST.get("öğrenci_ids")

    yoklamaTarihi = request.POST.get("yoklamaTarihi")
    yoklama = Katılım.objects.get(id=yoklamaTarihi)

    jsonÖğrenci = json.loads(öğrenci_ids)

    try:
        for öğre in jsonÖğrenci:
            öğrenci = Öğrenciler.objects.get(admin=öğre['id'])

            yoklamaRaporu = KatılımRaporu.objects.get(öğrenci_id=öğrenci,
                                                      yoklama_id=yoklama)
            yoklamaRaporu.status=öğre['status']

            yoklamaRaporu.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")
    
def çalışanProfili(request):
    user = CustomUser.objects.get(id=request.user.id)
    çalışan = Çalışanlar.objects.get(admin=user)

    context={
        "user":user,
        "çalışan":çalışan
    }
    return render(request, 'ÇalışanTemplate/çalışanProfili.html',context)

def çalışanProfiliGüncelleme(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('çalışanProfili')
    else:
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        şifre = request.POST.get('şifre')
        adres = request.POST.get('adres')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.ad = ad
            customuser.soyad = soyad
            if şifre != None and şifre != "":
                customuser.set_şifre(şifre)
            customuser.save()

            çalışan = Çalışanlar.objects.get(admin=customuser.id)
            çalışan.adres = adres
            çalışan.save()
            
            messages.success(request, "Profile Updated Successfully")
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('çalışanProfili')
    
def çalışanEklemeSonuç(request):
    konular = Konular.objects.filter(çalışan_id=request.user.id)
    sessionYılı = SessionYılModel.objects.all()
    context = {
        "konular":konular,
        "sessionYılı":sessionYılı,
    }
    return render(request, "ÇalışanTemplate/eklemeSonuçTemplate.html",context)

def çalışanEklemeSonuçKaydı(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method")
        return redirect('çalışanEklemeSonuç')
    else:
        öğrenciAdmin_id = request.POSt.get('öğrenciListesi')
        ödevNotları = request.POST.get('ödevNotları')
        sınavNotları = request.POST.get('sınavNotları')
        konu_id = request.POST.get('konu')

        öğrenciObj = Öğrenciler.objects.get(admin=öğrenciAdmin_id)
        konuObj = Konular.objects.get(id=konu_id)

        try:
            mevcutKontrol = ÖğrenciSonuçları.objects.filter(konu_id=konuObj,
                                                            öğrenci_id=öğrenciObj).exists()
            if mevcutKontrol:
                sonuç = ÖğrenciSonuçları.objects.get(konu_id=konuObj,
                                                     öğrenci_id=öğrenciObj)
                sonuç.konuÖdevNotu = ödevNotları
                sonuç.konuSınavNotu = sınavNotları
                sonuç.save()
                messages.success(request, "Sonuç Başarıyla Güncellendi!")
                return redirect('çalışanEklemeSonuç')
            else:
                sonuç = ÖğrenciSonuçları(öğrenci_id=öğrenciObj,
                                         konu_id=konuObj,
                                         konuSınavNotu=sınavNotları,
                                         konuÖdevNotu=ödevNotları)
                sonuç.save()
                messages.success(request, "Sonuç Başarıyla Eklendi!")
                return redirect('çalışanEklemeSonuç')
        except:
            messages.error(request, "Sonuç Eklerken Bir Hatayla Karşılaşıldı!")
            return redirect('çalışanEklemeSonuç')
            
    