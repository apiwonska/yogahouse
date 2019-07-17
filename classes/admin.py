from django.contrib import admin

from .models import ClassOffer, Conditions, PriceCategory, PriceDetail, PriceOption


class ClassOfferAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


class PriceCategoryAdmin(admin.ModelAdmin):
    readonly_field = ('created', 'updated')


class PriceOptionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


class ConditionsAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(ClassOffer, ClassOfferAdmin)
admin.site.register(PriceCategory, PriceCategoryAdmin)
admin.site.register(PriceDetail)
admin.site.register(PriceOption, PriceOptionAdmin)
admin.site.register(Conditions, ConditionsAdmin)
