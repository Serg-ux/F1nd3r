# Domain Query Tool based on SSL Certificates info
## Overview
This Python script queries the crt.sh database for SSL certificate information related to a given domain. 

## Script Usage

###  Run the Script with a Domain
To query certificates for a domain, simply pass the domain name as an argument:
```bash
python f1nd3r.py example.com
```

###  View Only Subdomains
To filter the results and show only the subdomains of the specified domain:
```bash
python f1nd3r.py example.com --subdomains
```

###  Show Subdomains with Their IP Addresses
If you want to see the IP addresses corresponding to each subdomain:
```bash
python f1nd3r.py example.com --subdomains --show-ips
```

###  Save the Results to a File
You can save the output to a file:
```bash
python f1nd3r.py example.com --save results.txt
```

###  Display the Command Wiki
If you need help using the script or want to see all available options:
```bash
python f1nd3r.py --wiki
```
