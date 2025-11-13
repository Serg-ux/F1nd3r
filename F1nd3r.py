i#!/usr/bin/env python3
"""
crt.sh Domain Lookup Tool
─────────────────────────
Query SSL certificate transparency logs for domains, extract subdomains,
resolve IPs, and save results — with beautiful colored output ✨
"""

import argparse
import json
import socket
import sys
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.syntax import Syntax

console = Console()


def show_help():
    """Displays a colorful command wiki."""
    help_text = """
[bold cyan]📘 Command Wiki[/bold cyan]

[bold yellow]Domain:[/bold yellow]
  The main argument should be the domain you want to query.
  Example:
    [green]python crtsh_lookup.py example.com[/green]

[bold yellow]--subdomains[/bold yellow]:
  Show only the subdomains related to the domain.
  Example:
    [green]python crtsh_lookup.py example.com --subdomains[/green]

[bold yellow]--show-ips[/bold yellow]:
  Show IP addresses for each subdomain.
  Example:
    [green]python crtsh_lookup.py example.com --subdomains --show-ips[/green]

[bold yellow]--save[/bold yellow]:
  Save results to a file.
  Example:
    [green]python crtsh_lookup.py example.com --save results.txt[/green]

[bold yellow]--wiki[/bold yellow]:
  Show this wiki page.

──────────────────────────────
Examples:
  [green]python crtsh_lookup.py example.com[/green]
  [green]python crtsh_lookup.py example.com --subdomains[/green]
  [green]python crtsh_lookup.py example.com --subdomains --show-ips[/green]
  [green]python crtsh_lookup.py example.com --save domains.txt[/green]
    """
    console.print(Panel(help_text, title="[bold cyan]crt.sh Helper[/bold cyan]", border_style="cyan"))
    sys.exit(0)


def fetch_crtsh_data(domain):
    """Fetch data from crt.sh."""
    url = f'https://crt.sh/?q={domain}&output=json'
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[bold red]❌ Error fetching data from crt.sh:[/bold red] {e}")
        sys.exit(1)


def extract_unique_names(data):
    """Extract unique domain names from crt.sh response."""
    names = [
        entry.get('name_value', '').strip('"')
        for entry in data if 'name_value' in entry
    ]
    names = [n for n in names if n and "CN=" not in n]
    return sorted(set(names))


def resolve_ip(subdomain):
    """Resolve IP address for a subdomain."""
    try:
        return socket.gethostbyname(subdomain)
    except socket.gaierror:
        return "IP not found"


def save_results(filename, data):
    """Save results to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, list):
                f.write('\n'.join(data))
            else:
                json.dump(data, f, indent=2)
        console.print(f"[bold green]💾 Results saved to:[/bold green] {filename}")
    except OSError as e:
        console.print(f"[bold red]❌ Error saving file:[/bold red] {e}")


def display_table(subdomains, show_ips):
    """Display subdomains (and optional IPs) in a rich table."""
    if not subdomains:
        console.print("[bold yellow]⚠️ No subdomains found.[/bold yellow]")
        return

    table = Table(
        title="🌐 Discovered Subdomains",
        box=box.ROUNDED,
        header_style="bold magenta"
    )
    table.add_column("Subdomain", style="cyan", no_wrap=True)
    if show_ips:
        table.add_column("IP Address", style="green")

    for sub in subdomains:
        if show_ips:
            ip = resolve_ip(sub)
            table.add_row(sub, ip)
        else:
            table.add_row(sub)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Query crt.sh for SSL certificate data of a domain.")
    parser.add_argument('domain', nargs='?', type=str, help='Domain to query (e.g., example.com)')
    parser.add_argument('--subdomains', action='store_true', help='Show only discovered subdomains.')
    parser.add_argument('--show-ips', action='store_true', help='Show IP addresses for subdomains.')
    parser.add_argument('--save', type=str, help='Save results to file.')
    parser.add_argument('--wiki', action='store_true', help='Display command wiki.')

    args = parser.parse_args()

    if args.wiki:
        show_help()

    if not args.domain:
        console.print("[bold red]❌ Error:[/bold red] Please provide a domain. Use [green]--wiki[/green] for help.")
        sys.exit(1)

    domain = args.domain

    console.print(Panel.fit(f"🔍 Querying [bold cyan]{domain}[/bold cyan] on crt.sh...", border_style="blue"))
    data = fetch_crtsh_data(domain)
    unique_names = extract_unique_names(data)

    if args.subdomains:
        subdomains = [n for n in unique_names if domain in n and n != domain]
        display_table(subdomains, args.show_ips)

        if args.save:
            save_results(args.save, subdomains)

    else:
        syntax = Syntax(json.dumps(data, indent=2), "json", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"📜 crt.sh Results for {domain}", border_style="green"))

        if args.save:
            save_results(args.save, data)


if __name__ == '__main__':
    main()
