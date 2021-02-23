from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('codigoInmueble','documentoIdentificacionArrendatario', 'valorPagado','fechaPago')
    search_fields = ['codigoInmueble', 'documentoIdentificacionArrendatario', ]
