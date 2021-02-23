from rest_framework.views import APIView
from rest_framework.response import Response
from apps.pagos.models import Pago
from rest_framework import status
from datetime import datetime
from django.db.models import Sum
"""
@author carlosacg 2020-12-11
API de Pagos
"""
class PagosApiView(APIView):
    name = 'pagos_api_view'

    def get(self, request, *args, **kwargs):
        """
        Lista todos los pagos almacenados en la base de datos
        """
        payments_lis = Pago.objects.all()
        data = []
        for pago in payments_lis:
            data.append({
                "documentoIdentificacionArrendatario":pago.documentoIdentificacionArrendatario,
                "codigoInmueble":pago.codigoInmueble,
                "valorPagado":pago.valorPagado,
                "fechaPago":datetime.strftime(pago.fechaPago,'%d/%m/%Y')
            })
        return Response(data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        params = request.data
        documentoIdentificacionArrendatario = params.get('documentoIdentificacionArrendatario',False)
        codigoInmueble = params.get('codigoInmueble',False)
        valorPagado = params.get('valorPagado',False)
        fechaPago = params.get('fechaPago',False)
        payment = Pago()
        mensaje = "gracias por pagar tu arriendo"

        try:
            fechaPago = datetime.strptime(fechaPago, '%d/%m/%Y')
            if fechaPago.day % 2 == 0:
                return Response("lo siento pero no se puede recibir el pago por decreto de administración",status=status.HTTP_400_BAD_REQUEST)
            else:
                payment.fechaPago = fechaPago
        except:
            return Response("Formato de fecha incorrecto",status=status.HTTP_400_BAD_REQUEST)

        try: 
            documentoIdentificacionArrendatario = int(documentoIdentificacionArrendatario)
            payment.documentoIdentificacionArrendatario = documentoIdentificacionArrendatario

        except:
            return Response("Formato de documento de identificacion incorrecto",status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            valorPagado = float(valorPagado)
            if valorPagado and valorPagado >= 1 and valorPagado <=1000000:
                payment.valorPagado = valorPagado
            else:
                return Response("El campo valorPagado debe estar entre 1 y 1000000",status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Formato de documento de valor pagado incorrecto",status=status.HTTP_400_BAD_REQUEST)

        try:           
            if codigoInmueble:
                payment.codigoInmueble = codigoInmueble 
            else:
                return Response("El campo codigoInmueble es obligatorio",status=status.HTTP_400_BAD_REQUEST)
            
            payment.save()
            if valorPagado == 1000000:
                mensaje='gracias por pagar todo tu arriendo'
            else:
                total_pagos_acumulados = 0
                lista_pagos_mes = Pago.objects.filter(
                    documentoIdentificacionArrendatario=documentoIdentificacionArrendatario,
                    codigoInmueble=codigoInmueble
                    )
                for pago_acumulado in lista_pagos_mes:
                    if pago_acumulado.fechaPago.month == fechaPago.month:
                        total_pagos_acumulados += pago_acumulado.valorPagado

                if total_pagos_acumulados >= 1000000:
                    mensaje='gracias por pagar todo tu arriendo'
                else:
                    mensaje='gracias por tu abono, sin embargo recuerda que te hace falta pagar ${diferencia}'.format(diferencia=1000000-total_pagos_acumulados)
            return Response(mensaje,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)