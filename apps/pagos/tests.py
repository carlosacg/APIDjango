from django.test import TestCase
import unittest
import requests
import json
"""
@author carlosacg 2020-12-11
Pruebas unitarias del API
"""
class TestApi(unittest.TestCase):
    def test_valor_valido(self):
        data = {'documentoIdentificacionArrendatario': '1234', 'codigoInmueble': '3312',"valorPagado":"1000000","fechaPago":"11/12/2020"}
        resp = requests.post('http://localhost:8084/api/pagos/', data=data)
        mensaje = resp.content.decode('utf-8')
        self.assertEqual("\"gracias por pagar todo tu arriendo\"",mensaje)

    def test_valor_invalido(self):
        data = {'documentoIdentificacionArrendatario': '1234', 'codigoInmueble': '3312',"valorPagado":"0","fechaPago":"11/12/2020"}
        resp = requests.post('http://localhost:8084/api/pagos/', data=data)
        mensaje = resp.content.decode('utf-8')
        self.assertEqual("\"El campo valorPagado debe estar entre 1 y 1000000\"",mensaje)
    
    def test_formato_fecha_invalido(self):
        data = {'documentoIdentificacionArrendatario': '1234', 'codigoInmueble': '3312',"valorPagado":"1000000","fechaPago":"11/20/2020"}
        resp = requests.post('http://localhost:8084/api/pagos/', data=data)
        mensaje = resp.content.decode('utf-8')
        self.assertEqual("\"Formato de fecha incorrecto\"",mensaje)

    def test_dia_pago_par(self):
        data = {'documentoIdentificacionArrendatario': '1234', 'codigoInmueble': '3312',"valorPagado":"1000000","fechaPago":"12/12/2020"}
        resp = requests.post('http://localhost:8084/api/pagos/', data=data)
        mensaje = resp.content.decode('utf-8')
        self.assertEqual("\"lo siento pero no se puede recibir el pago por decreto de administración\"",mensaje)

    

if __name__ == "__main__":
    unittest.main()
