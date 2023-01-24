from django.contrib import admin

from loyalty.models import Subscription, Order, Discount


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('enabled', 'period_begin', 'period_end',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'created_at')
