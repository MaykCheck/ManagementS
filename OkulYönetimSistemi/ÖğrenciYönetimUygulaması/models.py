from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
 

# Create your models here.


class SessionYılModel(models.Model):
    id = models.AutoField(primary_key=True)
    sessionBaşlangıçYılı = models.DateField()
    sessionBitişYılı = models.DateField()
    objects= models.Manager()

class CustomUser(AbstractUser):
    YÖNETİM = '1'
    ÇALIŞAN = '2'
    ÖĞRENCİ = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'yönetim':YÖNETİM,
        'çalışan':ÇALIŞAN,
        'öğrenci':ÖĞRENCİ
    }

    user_type_data = ((YÖNETİM, "YÖNETİM"),(ÇALIŞAN, "Çalışan"), (ÖĞRENCİ, "Öğrenci"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Yönetim(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Çalışanlar(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    adres = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Dersler(models.Model):
    id = models.AutoField(primary_key=True)
    dersAdı = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Konular(models.Model):
    id = models.AutoField(primary_key=True)
    konuAdı = models.CharField(max_length=255)

    ders_id = models.ForeignKey(Dersler, on_delete=models.CASCADE, default=1)
    çalışan_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Öğrenciler(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cinsiyet = models.CharField(max_length=50)
    profilFotoğrafı = models.FileField()
    adres = models.TextField()
    ders_id = models.ForeignKey(Dersler, on_delete=models.DO_NOTHING, default=1)
    sessionYılı_id = models.ForeignKey(SessionYılModel, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Katılım(models.Model):
    id = models.AutoField(primary_key=True)
    konu_id = models.ForeignKey(Konular, on_delete=models.DO_NOTHING)
    yoklamaTarihi = models.DateField()
    sessionYılı_id = models.ForeignKey(SessionYılModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class KatılımRaporu(models.Model):
    id = models.AutoField(primary_key=True)
    öğrenci_id = models.ForeignKey(Öğrenciler, on_delete=models.DO_NOTHING)
    yoklama_id = models.ForeignKey(Katılım, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÖğrenciİzinRaporu(models.Model):
    id = models.AutoField(primary_key=True)
    öğrenci_id = models.ForeignKey(Öğrenciler, on_delete=models.CASCADE)
    izinTarihi = models.CharField(max_length=255)
    izinMesajı = models.TextField()
    izin_status = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÇalışanİzinRaporu(models.Model):
    id = models.AutoField(primary_key=True)
    çalışan_id = models.ForeignKey(Çalışanlar, on_delete=models.CASCADE)
    izinTarihi = models.CharField(max_length=255)
    izinMesajı = models.TextField()
    izin_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
 

class ÖğrenciGeriBildirimi(models.Model):
    id = models.AutoField(primary_key=True)
    öğrenci_id = models.ForeignKey(Öğrenciler, on_delete=models.CASCADE)
    geriBildirim = models.TextField()
    geriBildirimCevabı = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÇalışanGeriBildirimi(models.Model):
    id = models.AutoField(primary_key=True)
    çalışan_id = models.ForeignKey(Çalışanlar, on_delete=models.CASCADE)
    geriBildirim = models.TextField()
    geriBildirimCevabı = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÖğrenciBildirimi(models.Model):
    id = models.AutoField(primary_key=True)
    öğrenci_id = models.ForeignKey(Öğrenciler, on_delete=models.CASCADE)
    mesaj = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÇalışanBildirimi(models.Model):
    id = models.AutoField(primary_key=True)
    çalışan_id = models.ForeignKey(Çalışanlar, on_delete=models.CASCADE)
    mesaj = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ÖğrenciSonuçları(models.Model):
    id = models.AutoField(primary_key=True)
    öğrenci_id = models.ForeignKey(Öğrenciler,on_delete=models.CASCADE)
    konu_id = models.AutoField(Konular, on_delete=models.CASCADE, default=1)
    konuSınavNotu = models.FloatField(default=0)
    konuÖdevNotu = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

@receiver(post_save, sender=CustomUser)
def kullanıcıProfiliOluştur(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Yönetim.objects.create(admin=instance)
        if instance.user_type == 2:
            Çalışanlar.objects.create(admin=instance)
        if instance.user_type == 3:
            Öğrenciler.objects.create(admin=instance,
                                      ders_id = Dersler.objects.get(id=1),
                                      sessionYılı_id = SessionYılModel.objects.get(id=1),
                                      adres = "",
                                      profilFotoğrafı = "",
                                      cinsiyet = "")
            
@receiver(post_save, sender=CustomUser)
def kullanıcıProfiliKaydet(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.yönetim.save()
    if instance.user_type == 2:
        instance.çalışan.save()
    if instance.user_type == 3:
        instance.öğrenci.save()