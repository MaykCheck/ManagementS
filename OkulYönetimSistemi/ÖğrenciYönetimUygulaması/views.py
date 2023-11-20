from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import CustomUser, Çalışanlar, Öğrenciler, Yönetim

# Create your views here.

def anasayfa(request):
    return render(request, 'anasayfa.html')

def iletişim(request):
    return render(request,'iletişim.html')

def kullanıcıGirişi(request):
    return render(request,'girişSayfası.html')

def girişYap(request):
    
    print("burası")
    email_id = request.GET.get('email')
    şifre = request.GET.get('şifre')
    
    print(email_id)
    print(şifre)
    print(request.user)
    if not (email_id and şifre):
        messages.error(request,"Lütfen istenen bilgileri giriniz!!")
        return render(request, 'girişSayfası.html')
    
    user = CustomUser.objects.filter(email=email_id, şifre=şifre).last()
    if not user:
        messages.error(request,'Giriş Bilgileriniz Yanlış!')
        return render(request,'girişSayfası.html')
    
    login(request, user)
    print(request.user)

    if user.user_type == CustomUser.ÖĞRENCİ:
        return redirect('öğrenciAnasayfa/')
    elif user.user_type == CustomUser.ÇALIŞAN:
        return redirect('çalışanAnasayfa/')
    elif user.user_type == CustomUser.YÖNETİM:
        return redirect('yönetimAnasayfa/')
    
    return render(request, 'anasayfa.html')

def kayıt(request):
    return render(request,'kayıt.html')

def kayıtOl(request):
    ad = request.GET.get('ad')
    soyad = request.GET.get('soyad')
    email_id = request.GET.get('email')
    şifre = request.GET.get('şifre')
    şifreDoğrula = request.GET.get('şifreDoğrula')

    print(email_id)
    print(şifre)
    print(şifreDoğrula)
    print(ad)
    print(soyad)
    if not (email_id and şifre and şifreDoğrula):
        messages.error(request,'Lütfen Bütün Bilgileri Giriniz!!')
        return render(request,'kayıt.html')
    
    if şifre != şifreDoğrula:
        messages.error(request,'Şifreleriniz Eşleşmiyor!!')
        return render(request,'kayıt.html')
    
    is_user_exists = CustomUser.objects.filter(email = email_id).exists()
    
    if is_user_exists:
        messages.error(request,'Bu Emaili Kullanan Bir Kullanıcı Zaten Var, Lütfen Giriş Yapınız!!')
        return render(request,'kayıt.html')
    
    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(request,"Lütfen Doğru Formatta Bir Email Giriniz: '<username>.<çalışan|öğrenci|yönetim>@<okul_domain>'")
        return render(request,'kayıt.html')
    
    username = email_id.split('@')[0].split('.')[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request,'Bu Kullanıcı Adıyla Zaten Bir Kullanıcı var, Lütfen Başka Kullanıcı Adı Deneyiniz.')
        return render(request,'kayıt.html')
    
    user = CustomUser()
    user.username = username
    user.email = email_id
    user.şifre = şifre
    user.user_type = user_type
    user.ad = ad
    user.soyad = soyad
    user.save()

    if user_type == CustomUser.ÇALIŞAN:
        Çalışanlar.objects.create(admin = user)
    elif user_type == CustomUser.ÖĞRENCİ:
        Öğrenciler.objects.create(admin = user)
    elif user_type == CustomUser.YÖNETİM:
        Yönetim.objects.create(admin = user)
    return render(request,'girişSayfası.hm')

def kullanıcıÇıkışı(request):
    logout(request)
    return HttpResponseRedirect('/')

def get_user_type_from_email(email_id):

    try:
        email_id = email_id.split('@')[0]
        email_user_type = email_id.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None