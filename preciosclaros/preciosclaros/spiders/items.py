# -*- coding: utf-8 -*-

import scrapy


class EmpresaItem(scrapy.Item):
    clase = 'empresa'
    uuid = scrapy.Field()
    nombre = scrapy.Field()


class SucursalItem(scrapy.Item):
    uuid = scrapy.Field()
    empresa_nombre = scrapy.Field()
    empresa_id = scrapy.Field()
    comercio_id = scrapy.Field()
    comercio_razon_social = scrapy.Field()
    direccion = scrapy.Field()
    _id = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    localidad = scrapy.Field()
    provincia = scrapy.Field()
    sucursal_id = scrapy.Field()
    sucursal_nombre = scrapy.Field()
    sucursal_tipo = scrapy.Field()


class ProductoItem(scrapy.Item):
    uuid = scrapy.Field()
    nombre = scrapy.Field()
    presentacion = scrapy.Field()
    _id = scrapy.Field()
    marca = scrapy.Field()


class ProductoSucursalPrecioItem(scrapy.Item):
    uuid = scrapy.Field()
    producto_id = scrapy.Field()
    sucursal_id = scrapy.Field()
    precio = scrapy.Field()
