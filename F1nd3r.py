import requests
import json
import argparse
import sys

# Función para mostrar la wiki de comandos
def show_help():
    help_text = """
    --- Wiki de Comandos ---

    - **Dominio**: El argumento principal debe ser un dominio que deseas consultar. 
      Ejemplo:
      python script.py example.com
      Este comando consulta la base de datos crt.sh para obtener los certificados asociados al dominio.
      
    - **--subdomains**: Muestra solo los subdominios del dominio especificado.
      Ejemplo:
      python script.py example.com --subdomains
      Este comando filtra los resultados para mostrar solo los subdominios relacionados con el dominio proporcionado.
      
    - **--wiki**: Muestra esta wiki de comandos.
    
    --- Ejemplos ---
    
    Para consultar un dominio y ver los certificados:
    python script.py example.com

    Para consultar solo los subdominios de un dominio:
    python script.py example.com --subdomains
    """
    print(help_text)
    sys.exit(0)

# Configurar el parser de argumentos
parser = argparse.ArgumentParser(description='Consulta crt.sh para un dominio y procesa los resultados.')
parser.add_argument('domain', nargs='?', type=str, help='El dominio que deseas consultar (por ejemplo, example.com)')
parser.add_argument('--subdomains', action='store_true', help='Solo muestra los subdominios encontrados.')
parser.add_argument('--wiki', action='store_true', help='Muestra una wiki de los comandos')

# Parsear los argumentos
args = parser.parse_args()

# Si se pasa el argumento --wiki, muestra la wiki
if args.wiki:
    show_help()

# Si no se pasa el dominio, mostrar un error de uso
if not args.domain:
    print("Por favor, proporciona un dominio. Usa --wiki para ver las opciones.")
    sys.exit(1)

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

    # Si se pasó --subdomains, filtrar solo los subdominios
    if args.subdomains:
        subdomains = [name for name in unique_names if domain in name and name != domain]
        # Imprimir solo los subdominios
        for subdomain in subdomains:
            print(subdomain)
    else:
        # Mostrar el JSON completo como si fuera un `curl` con `jq`
        print(json.dumps(data, indent=2))

else:
    print(f"Error al hacer la solicitud: {response.status_code}")
