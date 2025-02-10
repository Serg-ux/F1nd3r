import requests
import json
import argparse

# Configurar el parser de argumentos
parser = argparse.ArgumentParser(description='Consulta crt.sh para un dominio y procesa los resultados.')
parser.add_argument('domain', type=str, help='El dominio que deseas consultar (por ejemplo, google.com)')

# Parsear los argumentos
args = parser.parse_args()

# Obtener el dominio desde los argumentos
domain = args.domain

# Hacer la solicitud GET a crt.sh
url = f'https://crt.sh/?q={domain}&output=json'
response = requests.get(url)

# Si la solicitud fue exitosa
if response.status_code == 200:
    # Convertir la respuesta JSON
    data = response.json()
    
    # Extraer todos los valores de "name" de cada entrada
    names = []
    for entry in data:
        name = entry.get('name_value', '')
        if name and "CN=" not in name:
            names.append(name.strip('"'))
    
    # Eliminar duplicados y ordenar los resultados
    unique_names = sorted(set(names))

    # Imprimir el resultado
    for name in unique_names:
        print(name)

else:
    print(f"Error al hacer la solicitud: {response.status_code}")