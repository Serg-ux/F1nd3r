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