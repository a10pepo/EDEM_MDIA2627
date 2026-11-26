import sys

with open('ventas.json') as archivo:
    contenido = archivo.read().lower()

if 'api_key' in contenido:
    print('Error: posible clave API expuesta en ventas.json')
    sys.exit(1)

print('No se han encontrado claves API expuestas')
