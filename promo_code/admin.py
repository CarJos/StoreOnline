from django.contrib import admin
from promo_code.models import PromoCode

class PromoCodeAdmin(admin.ModelAdmin):
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)