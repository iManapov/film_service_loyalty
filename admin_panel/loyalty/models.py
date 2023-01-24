import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from config import settings


class Status(models.IntegerChoices):
    CREATED = 0, _('CREATED')
    IN_PROCESS = 1, _('IN_PROCESS')
    PAID = 2, _('PAID')
    CANCELED = 3, _('CANCELED')


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subscription(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True, null=True)
    price = models.FloatField(_('price'), validators=[MinValueValidator(0),])
    months = models.IntegerField(_('months'), validators=[MinValueValidator(0),])

    def __str__(self):
        return self.name

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"subscription"
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class Discount(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=50)
    subscription = models.ForeignKey(Subscription,
                                     verbose_name=_('subscription'),
                                     on_delete=models.CASCADE)
    value = models.IntegerField(_('value'), validators=[MinValueValidator(0),])
    enabled = models.BooleanField(_('enabled'), default=False)
    period_begin = models.DateField(_('start_date'))
    period_end = models.DateField(_('end_date'))

    def __str__(self):
        return _(f'Discount {self.id}')

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"discount"
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')


class Order(UUIDMixin, TimeStampedMixin):
    discount = models.ForeignKey(Subscription,
                                 verbose_name=_('subscription'),
                                 on_delete=models.DO_NOTHING)
    user = models.UUIDField(_('user'), editable=False)
    status = models.IntegerField(_('status'), choices=Status.choices)
    amount = models.IntegerField(_('amount'), validators=[MinValueValidator(0),])

    def __str__(self):
        return _(f'Order {self.id}')

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"order"
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


