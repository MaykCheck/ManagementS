from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import CustomUser, Çalışanlar, Dersler, Konular, Öğrenciler, Katılım, KatılımRaporu, ÖğrenciİzinRaporu, ÖğrenciGeriBildirimi, ÖğrenciSonuçları


def öğrenciAnasayfa(request):
    öğrenciObj = Öğrenciler.objects.get(admin=request.user.id)
    toplamKatılım = KatılımRaporu.objects.filter(öğrenci_id=öğrenciObj).count()
    mevcutKatılım = KatılımRaporu.objects.filter(öğrenci_id=öğrenciObj, status=True).count()
    eksikKatılım = KatılımRaporu.objects.filter(öğrenci_id=öğrenciObj, status=False).count()
    dersObj = Dersler.objects.get(id=öğrenciObj.ders_id.id)
    toplamKonu = Konular.objects.filter(ders_id=dersObj).count()
    konuAdı = []
    mevcutData = []
    eksikData = []
    konuData = Konular.objects.filter(ders_id=öğrenciObj.ders_id)
    for konu in konuData:
        katılım = Katılım.objects.filter(konu_id=konu.id)
        mevcutKatılımSayısı = KatılımRaporu.objects.filter(yoklama_id__in=katılım, status=True, öğrenci_id=öğrenciObj.id).count()
        eksikKatılımSayısı = KatılımRaporu.objects.filter(yoklama_id__in=katılım, status=False,öğrenci_id=öğrenciObj.id).count()
        konuAdı.append(konu.konuAdı)
        mevcutData.append(mevcutKatılımSayısı)
        eksikData.append(eksikKatılımSayısı)

        context={
            "toplamKatılım":toplamKatılım,
            "mevcutKatılım":mevcutKatılım,
            "eksikKatılım":eksikKatılım,
            "toplamKonu":toplamKonu,
            "konuAdı":konuAdı,
            "mevcutData":mevcutData,
            "eksikData":eksikData
        }
        return render(request,"ÖğrenciTemplate/öğrenciAnasayfaTemplate.html")
    
def öğrenciViewKatılım(request):
    öğrenci = Öğrenciler.object.get(admin=request.user.id)
    ders = öğrenci.ders_id
    konular = Konular.objects.filter(ders_id=ders)
    context = {
        "konular":konular
    }
    return render(request,"ÖğrenciTemplate/öğrenciViewKatılım.html",context)

def öğrenciViewKatılımPost(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method")
        return redirect('öğrenciViewKatılım')
    else:
        konu_id = request.POST.get('konu')
        başlangıçTarihi = request.POST.get('başlangıçTarihi')
        bitişTarihi = request.POST.get('bitişTarihi')

        başlangıçTarihiParse = datetime.datetime.strptime(başlangıçTarihi, '%Y-%m-%d').date()
        bitişTarihiParse = datetime.datetime.strptime(bitişTarihi, '%Y-%m-%d').date()

        konuObj = Konular.objects.get(id=konu_id)
        userObj = CustomUser.objects.get(id=request.user.id)
        öğreObj = Öğrenciler.objects.get(admin=userObj)
        katılım = Katılım.objects.filter(yoklamaTarihi__range=(başlangıçTarihiParse,bitişTarihiParse), konu_id=konuObj)
        katılım_raporları = KatılımRaporu.objects.filter(yoklama_id__in=katılım, öğrenci_id=öğreObj)
        context = {
            "konuObj":konuObj,
            "katılım_raporları":katılım_raporları
        }
        return render(request,'ÖğrenciTemplate/öğrenciKatılımData.html',context)
    
def öğrenciİzinTalebi(request):
    öğrenciObj = Öğrenciler.objects.get(admin=request.user.id)
    izinData = ÖğrenciİzinRaporu.objects.filter(öğrenci_id=öğrenciObj)
    context = {
        "izinData":izinData
    }
    return render(request,'ÖğrenciTemplate/öğrenciİzinTalebi.html',context)

def öğrenciİzinTalebiKaydı(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('öğrenciİzinTalebi')
    else:
        izinTarihi = request.POST.get('izinTarihi')
        izinMesajı = request.POST.get('izinMesajı')
        öğrenciObj = Öğrenciler.objects.get(admin=request.user.id)
        try:
            izinRaporu = ÖğrenciİzinRaporu(öğrenci_id=öğrenciObj,
                                           izinTarihi=izinTarihi,
                                           izinMesajı=izinMesajı,
                                           izin_status=0)
            izinRaporu.save()
            messages.success(request,"Applied for Leave.")
            return redirect('öğrenciİzinTalebi')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('öğrenciİzinTalebi')

def öğrenciGeriBildirimi(request):
    öğrenciObj = Öğrenciler.objects.get(admin=request.user.id)
    geriBildirimData = ÖğrenciGeriBildirimi.objects.filter(öğrenci_id=öğrenciObj)
    context = {
        "geriBildirimData":geriBildirimData
    }
    return render(request,'ÖğrenciTemplate/öğrenciGeriBildirimi.html',context)

def öğrenciGeriBildirimiKaydı(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('öğrenciGeriBildirimi')
    else:
        geriBildirim = request.POST.get('geriBildirimMesajı')
        öğrenciObj = Öğrenciler.objects.get(admin=request.user.id)

        try:
            geriBildirimEkle = ÖğrenciGeriBildirimi(öğrenci_id=öğrenciObj,
                                                    geriBildirim=geriBildirim,
                                                    geriBildirimCevabı="")
            geriBildirimEkle.save()
            messages.succes(request,"Feedback Sent.")
            return redirect('öğrenciGeribildirimi')
        except:
            messages.error(request,"Failed to Send Feedback.")
            return redirect('öğrenciGeriBildirimi')
        
def öğrenciProfili(request):
    user = CustomUser.objects.get(id=request.user.id)
    öğrenci = Öğrenciler.objects.get(admin=user)

    context={
        "user":user,
        "öğrenci":öğrenci
    }
    return render(request, 'ÖğrenciTemplate/öğrenciProfili.html', context)

def öğrenciProfiliGüncelleme(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('öğrenciProfili')
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

            öğrenci = Öğrenciler.objects.get(admin=customuser.id)
            öğrenci.adres = adres
            öğrenci.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('öğrenciProfili')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('öğrenciProfili')

def öğrenciViewSonuç(request):
    öğrenci = Öğrenciler.objects.get(admin=request.user.id)
    öğrenciSonuç = ÖğrenciSonuçları.objects.filter(öğrenci_id=öğrenci.id)
    context = {
        "öğrenciSonuç":öğrenciSonuç
    }
    return render(request, "ÖğrenciTemplate/öğrenciViewSonuç.html",context)