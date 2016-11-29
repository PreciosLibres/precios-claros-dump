#!/usr/bin/python

import requests
import urllib

headers = {'x-api-key': 'zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96'}
empresas = requests.get('https://8kdx6rx8h4.execute-api.us-east-1.amazonaws.com/prod/filtros?field=comercio_bandera_nombre', headers=headers).json()['valoresFiltrables']

for empresa in empresas:
    print 'procesando empresa ' + empresa
    requests.post('http://127.0.0.1:5984/empresa', json={'nombre': empresa})
    sucursales = []
    total = 999
    while (len(sucursales) < total):
        print 'sucursales obtenidas ' + str(len(sucursales))
        sucursales_response = requests.get(
            'https://8kdx6rx8h4.execute-api.us-east-1.amazonaws.com/prod/sucursales?lat=-34.5847744&lng=-58.4046195&limit=30&comercio_bandera_nombre=["' + urllib.quote_plus(empresa) + '"]',
            headers=headers).json()
        total = sucursales_response['total']

        sucursales += sucursales_response['sucursales']

    for sucursal in sucursales:
        sucursal['empresa'] = empresa
        requests.post('http://127.0.0.1:5984/sucursal', json=sucursal)

for sucursal in sucursales:
    print 'procesando sucursal ' + sucursal['id']
    productos = []
    total = 999

    while (len(productos) < total):
        print 'productos obtenidos' + str(len(productos))
        productos_response = requests.get(
            'https://8kdx6rx8h4.execute-api.us-east-1.amazonaws.com/prod/productos?&array_sucursales=' + sucursal['id'] + '&limit=50&offset=' + str(len(productos)),
            headers=headers).json()
        total = productos_response['total']
        productos += productos_response['productos']

    for producto in productos:
        producto['sucursal'] = sucursal['id']
        requests.post('http://127.0.0.1:5984/producto', json=producto)
