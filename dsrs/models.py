# django imports
from django.db import models


class Territory(models.Model):
    name            = models.CharField(max_length=48, default='Spain')
    code_2          = models.CharField(max_length=2, default='ES')
    code_3          = models.CharField(max_length=3)
    local_currency  = models.ForeignKey(
                        to           = 'Currency',
                        on_delete    = models.CASCADE,
                        related_name = 'territories',
                        )

    class Meta:
        ordering            = ("name",)
        db_table            = 'territory'
        verbose_name        = 'territory'
        verbose_name_plural = 'territories'

    def __str__(self):
        return self.name


class Currency(models.Model):
    name    = models.CharField(max_length=48, default='Euro')
    code    = models.CharField(max_length=3, default='EUR')
    symbol  = models.CharField(max_length=4)

    class Meta:
        db_table            = "currency"
        verbose_name        = "currency"
        verbose_name_plural = "currencies"

    def __str__(self):
        return self.name


class DSR(models.Model):
    STATUS_ALL = (
        ("ingested", "INGESTED"),
        ("failed", "FAILED"),
    )
    path            = models.CharField(max_length=256)
    period_end      = models.DateField(null=False)
    period_start    = models.DateField(null=False)
    status          = models.CharField(
                        choices     = STATUS_ALL,
                        default     = STATUS_ALL[0][0],
                        max_length  = 48,
                        )
    territory       = models.ForeignKey(
                        to           = Territory,
                        on_delete    = models.CASCADE,
                        related_name = "dsrs"
                        )
    currency        = models.ForeignKey(
                        to           = Currency,
                        on_delete    = models.CASCADE,
                        related_name = "dsrs"
                        )
    class Meta:
        db_table            = "dsr"
        verbose_name        = 'dsr'
        verbose_name_plural = 'dsrs'

    def __str__(self):
        return self.path

class Resource(models.Model):
    dsp_id          = models.CharField(max_length=256)
    usages          = models.IntegerField(default=0)
    revenue         = models.BigIntegerField(default=0)
    isrc            = models.CharField(max_length=256, null=True, blank=True)
    title           = models.CharField(max_length=256, null=True, blank=True)
    artists         = models.CharField(max_length=256, null=True, blank=True)
    dsr             = models.ManyToManyField(
                        to           = DSR,
                        related_name = "resource"
                        )
    class Meta:
        db_table            = "resource"
        verbose_name        = 'resource'
        verbose_name_plural = 'resources'

    def __str__(self):
        return self.dsp_id
