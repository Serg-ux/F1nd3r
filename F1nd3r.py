import requests
import json
import argparse
import sys
import socket
import os

# Function to display the command wiki
def show_help():
    help_text = """
    --- Command Wiki ---

    - **Domain**: The main argument should be a domain you want to query. 
      Example:
      python script.py example.com
      This command queries the crt.sh database to get certificates associated with the domain.
      
    - **--subdomains**: Displays only the subdomains of the specified domain.
      Example:
      python script.py example.com --subdomains
      This command filters the results to show only the subdomains related to the provided domain.
      
    - **--show-ips**: Shows the IP addresses of subdomains for the specified domain.
      Example:
      python script.py example.com --subdomains --show-ips
      This command shows the subdomains and their corresponding IP addresses.
      
    - **--save**: Saves the results of the query into a file specified by the user.
      Example:
      python script.py example.com --save myfile.txt
      This command saves the results of the domain query in the file specified.

    - **--wiki**: Displays this command wiki.
    
    --- Examples ---
    
    To query a domain and view the certificates:
    python script.py example.com

    To query only the subdomains of a domain:
    python script.py example.com --subdomains

    To show subdomains and their IP addresses:
    python script.py example.com --subdomains --show-ips

    To save the results to a specific file:
    python script.py example.com --save myfile.txt

    To save the results and display only subdomains:
    python script.py example.com --subdomains --save myfile.txt
    """
    print(help_text)
    sys.exit(0)

# Set up the argument parser
parser = argparse.ArgumentParser(description='Query crt.sh for a domain and process the results.')
parser.add_argument('domain', nargs='?', type=str, help='The domain you want to query (e.g., example.com)')
parser.add_argument('--subdomains', action='store_true', help='Only display the found subdomains.')
parser.add_argument('--show-ips', action='store_true', help='Show the IP addresses of subdomains.')
parser.add_argument('--save', type=str, help='Save the results to a file (default is scan.txt).')
parser.add_argument('--wiki', action='store_true', help='Displays a wiki of the commands')

# Parse the arguments
args = parser.parse_args()

# If the --wiki argument is passed, show the wiki
if args.wiki:
    show_help()

# If no domain is passed, show a usage error
if not args.domain:
    print("Please provide a domain. Use --wiki to see the options.")
    sys.exit(1)

# Get the domain from the arguments
domain = args.domain

# Make the GET request to crt.sh
url = f'https://crt.sh/?q={domain}&output=json'
response = requests.get(url)

# If the request was successful
if response.status_code == 200:
    # Convert the JSON response
    data = response.json()
    
    # Extract all the "name" values from each entry
    names = []
    for entry in data:
        name = entry.get('name_value', '')
        if name and "CN=" not in name:
            names.append(name.strip('"'))
    
    # Remove duplicates and sort the results
    unique_names = sorted(set(names))

    # If --subdomains was passed, filter only the subdomains
    subdomains = []
    if args.subdomains:
        subdomains = [name for name in unique_names if domain in name and name != domain]
        
        # Print the subdomains and, if --show-ips is passed, show their IP addresses
        if args.show_ips:
            for subdomain in subdomains:
                try:
                    ip = socket.gethostbyname(subdomain)
                    print(f"{subdomain} -> {ip}")
                except socket.gaierror:
                    print(f"{subdomain} -> IP not found")
        else:
            # Print only the subdomains
            for subdomain in subdomains:
                print(subdomain)

    else:
        # Display the full JSON response
        print(json.dumps(data, indent=2))

    # If --save was passed, save the results to the file specified by the user
    if args.save:
        file_name = args.save if args.save else 'scan.txt'  # Default to 'scan.txt' if no filename is given
        with open(file_name, 'w') as file:
            if subdomains:
                for subdomain in subdomains:
                    file.write(f"{subdomain}\n")
            else:
                file.write(json.dumps(data, indent=2))
        print(f"Results saved to {file_name}")
else:
    print(f"Error making the request: {response.status_code}")