from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Yönetim, Çalışanlar, Dersler, Konular, Öğrenciler, Katılım, KatılımRaporu, ÖğrenciİzinRaporu, ÇalışanİzinRaporu, ÇalışanGeriBildirimi, ÖğrenciGeriBildirimi, ÖğrenciBildirimi, ÇalışanBildirimi

# Register your models here.

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Yönetim)
admin.site.register(Çalışanlar)
admin.site.register(Öğrenciler)
admin.site.register(Dersler)
admin.site.register(Konular)
admin.site.register(Katılım)
admin.site.register(KatılımRaporu)
admin.site.register(ÖğrenciİzinRaporu)
admin.site.register(ÇalışanİzinRaporu)
admin.site.register(ÖğrenciGeriBildirimi)
admin.site.register(ÇalışanGeriBildirimi)
admin.site.register(ÖğrenciBildirimi)
admin.site.register(ÇalışanBildirimi)