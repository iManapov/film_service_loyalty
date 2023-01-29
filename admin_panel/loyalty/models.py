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


class Measure(models.TextChoices):
    PERCENT = _('%'), _('%')
    RUB = _('RUB'), _('RUB')


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


class DiscountSubscription(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=50)
    subscription = models.ForeignKey(Subscription,
                                     verbose_name=_('subscription'),
                                     on_delete=models.CASCADE)
    value = models.IntegerField(_('value'), validators=[MinValueValidator(0),])
    enabled = models.BooleanField(_('enabled'), default=False)
    period_begin = models.DateTimeField(_('start_date'))
    period_end = models.DateTimeField(_('end_date'))

    def __str__(self):
        return f"{_('SubscriptionDiscount')} {self.id}"

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"discount_subscription"
        verbose_name = _('Subscription discount')
        verbose_name_plural = _('Subscription discounts')


class DiscountFilms(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=50)
    tag = models.CharField(_('tag'), max_length=50)
    subscription = models.ForeignKey(Subscription,
                                     verbose_name=_('subscription'),
                                     on_delete=models.CASCADE)
    value = models.IntegerField(_('value'), validators=[MinValueValidator(0),])
    enabled = models.BooleanField(_('enabled'), default=False)
    period_begin = models.DateTimeField(_('start_date'))
    period_end = models.DateTimeField(_('end_date'))

    def __str__(self):
        return f"{_('FilmDiscount')} {self.id}"

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"discount_film"
        verbose_name = _('Film discount')
        verbose_name_plural = _('Film discounts')


class Promocode(UUIDMixin, TimeStampedMixin):
    user_id = models.UUIDField(_('user'))
    value = models.FloatField(_('value'), validators=[MinValueValidator(0),])
    code = models.CharField(_('code'), max_length=50)
    expiration_date = models.DateTimeField(_('expiration_date'))
    measure = models.CharField(_('measure'), max_length=5, choices=Measure.choices)
    is_multiple = models.BooleanField(_('is_multiple'), default=False)

    def __str__(self):
        return f"{_('Promocode')} {self.id}"

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"promocode"
        verbose_name = _('Promocode')
        verbose_name_plural = _('Promocodes')


class PromoUsage(UUIDMixin, TimeStampedMixin):
    promo = models.ForeignKey(Promocode,
                              verbose_name=_('promo'),
                              on_delete=models.CASCADE)
    user_id = models.UUIDField(_('user'))
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{_('User ')} {self.user_id} {_(' used promocode ')} {self.promo}"

    class Meta:
        db_table = f"{settings.DB_SCHEME}\".\"promo_usage"
        verbose_name = _('PromoUsage')
        verbose_name_plural = _('PromoUsages')
