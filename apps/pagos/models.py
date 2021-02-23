from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
"""
@author carlosacg 2020-12-11
Modelo de Pago
"""
class Pago(models.Model):
    fechaPago = models.DateField(verbose_name=_('fecha de pago'))
    documentoIdentificacionArrendatario = models.BigIntegerField(null=True, blank=True, verbose_name=_('id arrendatario'))
    codigoInmueble = models.TextField(blank=True, verbose_name=_('codigo inmueble'))
    valorPagado = models.FloatField(validators = [MinValueValidator(1), MaxValueValidator(1000000)])

    class Meta:
        verbose_name = _('Pago')
        verbose_name_plural = _('Pagos')

