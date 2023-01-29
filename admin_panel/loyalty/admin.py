from django.contrib import admin

from loyalty.models import Subscription, DiscountSubscription, \
    DiscountFilms, Promocode, PromoUsage


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(DiscountSubscription)
class DiscountSubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('enabled', 'period_begin', 'period_end',)


@admin.register(DiscountFilms)
class DiscountFilmsAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('enabled', 'period_begin', 'period_end',)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_filter = ('value', 'expiration_date',)


@admin.register(PromoUsage)
class PromoUsageAdmin(admin.ModelAdmin):
    search_fields = ('promo',)
