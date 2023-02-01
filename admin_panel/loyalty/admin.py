from django.contrib import admin

from loyalty.models import Subscription, DiscountSubscription, \
    DiscountFilm, Promocode, PromoUsage, DiscountSubscriptionUsage, \
    DiscountFilmUsage


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'months', 'price',)


@admin.register(DiscountSubscription)
class DiscountSubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('enabled', 'period_begin', 'period_end',)
    list_display = ('title', 'value', 'enabled',)


@admin.register(DiscountFilmUsage)
class DiscountFilmUsageAdmin(admin.ModelAdmin):
    search_fields = ('user_id',)
    list_filter = ('used_at',)
    list_display = ('discount', 'user_id', 'used_at',)


@admin.register(DiscountFilm)
class DiscountFilmAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('enabled', 'period_begin', 'period_end',)
    list_display = ('title', 'value', 'enabled',)


@admin.register(DiscountSubscriptionUsage)
class DiscountSubscriptionUsageAdmin(admin.ModelAdmin):
    search_fields = ('user_id',)
    list_filter = ('used_at',)
    list_display = ('user_id', 'discount', 'used_at',)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_filter = ('value', 'expiration_date',)
    list_display = ('code', 'user_id', 'is_multiple',)


@admin.register(PromoUsage)
class PromoUsageAdmin(admin.ModelAdmin):
    search_fields = ('promo',)
    list_display = ('user_id', 'promo', 'used_at',)
