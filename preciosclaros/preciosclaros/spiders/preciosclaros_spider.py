import math
import json
import urllib
import datetime
import scrapy
import items

BASE_URL = 'https://8kdx6rx8h4.execute-api.us-east-1.amazonaws.com/prod/'

class PreciosClarosSpider(scrapy.Spider):
    name = "preciosclaros"

    start_urls = [BASE_URL + 'filtros?field=comercio_bandera_nombre']

    def parse(self, response):
        empresas = json.loads(response.body_as_unicode())['valoresFiltrables']

        for nombre in empresas:

            yield items.EmpresaItem(
                uuid   = 'empresa-' + nombre,
                nombre = nombre,
            )

            sucursales_url = BASE_URL + 'sucursales?limit=100&comercio_bandera_nombre=["' + urllib.quote_plus(nombre) + '"]'

            request = scrapy.Request(sucursales_url, callback=self.parse_primera_sucursales)
            request.meta['empresa_nombre'] = nombre

            yield request

    def parse_primera_sucursales(self, response):
        self.parse_content_sucursales(response)

        total = json.loads(response.body_as_unicode())['total']

        if total > 1:

            for index in range(2, int(math.ceil(total/100.))):

                sucursales_url = BASE_URL + 'sucursales?limit=100&offset=' + str(index * 100) + '&comercio_bandera_nombre=["' + urllib.quote_plus(response.meta['empresa_nombre']) + '"]'

                yield scrapy.Request(sucursales_url, callback=self.parse_content_sucursales)

    def parse_content_sucursales(self, response):
        json_response = json.loads(response.body_as_unicode())

        sucursales = json_response['sucursales']

        for sucursal in sucursales:

            yield items.SucursalItem(
                _id                   = sucursal['id'],
                uuid                  = "sucursal-" + sucursal['id'],
                empresa_nombre        = sucursal['banderaDescripcion'],
                empresa_id            = sucursal['banderaId'],
                comercio_id           = sucursal['comercioId'],
                comercio_razon_social = sucursal['comercioRazonSocial'],
                direccion             = sucursal['direccion'],
                lat                   = sucursal['lat'],
                lng                   = sucursal['lng'],
                localidad             = sucursal['localidad'],
                provincia             = sucursal['provincia'],
                sucursal_id           = sucursal['sucursalId'],
                sucursal_nombre       = sucursal['sucursalNombre'],
                sucursal_tipo         = sucursal['sucursalTipo']
            )

            productos_url = BASE_URL + 'productos?&id_sucursal=' + sucursal['id'] + '&limit=100&offset=0'

            request = scrapy.Request(productos_url, callback=self.parse_primera_productos)
            request.meta['sucursal_id'] = sucursal['id']

            yield request

    def parse_primera_productos(self, response):
        sucursal_id = response.meta['sucursal_id']

        self.parse_content_productos(response)

        total = json.loads(response.body_as_unicode())['total']

        if total > 1:

            for index in range(2, int(math.ceil(total/100.))):

                productos_url = BASE_URL + 'productos?limit=100&offset=' + str(index * 100) + '&id_sucursal=' + sucursal_id
            	request = scrapy.Request(productos_url, callback=self.parse_content_productos)
            	request.meta['sucursal_id'] = sucursal_id

                yield request

    def parse_content_productos(self, response):
        sucursal_id = response.meta['sucursal_id']

        json_response = json.loads(response.body_as_unicode())

        productos = json_response['productos']

        for producto in productos:

            yield items.ProductoItem(
                _id          = producto['id'],
                uuid         = "producto-" + producto['id'],
                nombre       = producto['nombre'],
                presentacion = producto['presentacion'],
                marca        = producto['marca']
            )

            yield items.ProductoSucursalItem(
                uuid        = 'productosucursalitem-' + producto['id'] + '-' + sucursal_id,
                producto_id = producto['id'],
                sucursal_id = sucursal_id
                precio      = producto['precio'],
                relevado_en = datetime.datetime.now().strftime("%m-%d-%Y")
            )
