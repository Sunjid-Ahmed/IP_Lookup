#!/usr/bin/env python3

import requests
import socket
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def reverse_dns(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "No PTR record found"
    except Exception as e:
        return f"Error: {e}"

def get_ip_info(ip):
    try:
        headers = {"User-Agent": "IPInfoLookupTool/1.0"}
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5, headers=headers)
        data = res.json()

        if data["status"] != "success":
            console.print(f"[bold red]❌ Error:[/bold red] {data.get('message', 'Failed to retrieve data')}")
            return

        hostname = reverse_dns(ip)

        table = Table(title=f"🌍 IP Information for {ip}", box=box.SIMPLE_HEAVY)
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="green")

        table.add_row("Hostname (PTR)", hostname)
        table.add_row("Country", f"{data['country']} ({data['countryCode']})")
        table.add_row("Region", f"{data['regionName']} ({data['region']})")
        table.add_row("City", data['city'])
        table.add_row("ZIP Code", data['zip'])
        table.add_row("Timezone", data['timezone'])
        table.add_row("Latitude", str(data['lat']))
        table.add_row("Longitude", str(data['lon']))
        table.add_row("ISP", data['isp'])
        table.add_row("Organization", data['org'])
        table.add_row("AS", data['as'])
        table.add_row("Mobile", "Yes" if data['mobile'] else "No")
        table.add_row("Proxy", "Yes" if data['proxy'] else "No")
        table.add_row("Hosting", "Yes" if data['hosting'] else "No")

        console.print(table)
        map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        console.print(Panel.fit(f"[bold yellow]📍 Google Maps:[/bold yellow] [underline blue]{map_url}[/underline blue]", title="View on Map", box=box.ROUNDED))

    except requests.RequestException as e:
        console.print(f"[bold red]❌ Request error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error:[/bold red] {e}")

def main():
    parser = argparse.ArgumentParser(description="🔍 IP Information Lookup Tool (like mini-nmap)")
    
    console.print("""[bold magenta]

 ██▓ ██▓███   ▄▄▄       ▄████▄   ██▓    ▓█████  ▒██   ██▒ ██▓ ██▓███  
▓██▒▓██░  ██▒▒████▄    ▒██▀ ▀█  ▓██▒    ▓█   ▀  ▒▒ █ █ ▒░▓██▒▓██░  ██▒
▒██▒▓██░ ██▓▒▒██  ▀█▄  ▒▓█    ▄ ▒██░    ▒███    ░░  █   ░▒██▒▓██░ ██▓▒
░██░▒██▄█▓▒ ▒░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒██░    ▒▓█  ▄   ░ █ █ ▒ ░██░▒██▄█▓▒ ▒
░██░▒██▒ ░  ░ ▓█   ▓██▒▒ ▓███▀ ░░██████▒░▒████▒▒██▒ ▒██▒░██░▒██▒ ░  ░
░▓  ▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░░ ▒░▓  ░░░ ▒░ ░▒▒ ░ ░▓ ░░▓  ▒▓▒░ ░  ░
 ▒ ░░▒ ░       ▒   ▒▒ ░  ░  ▒   ░ ░ ▒  ░ ░ ░  ░░░   ░▒ ░ ▒ ░░▒ ░     
 ▒ ░░░         ░   ▒   ░          ░ ░      ░    ░    ░   ▒ ░░░       
 ░               ░  ░ ░ ░          ░  ░   ░  ░ ░    ░   ░           
                      ░                                               
             [ IP LOOKUP TOOL - Trace IP, Find Location, ISP, and More ]
[/bold magenta]""")
    console.print("[bold cyan]A CLI tool to fetch IP details like a mini-Nmap[/bold cyan]")
    console.print("[bold yellow]Author:[/bold yellow] Sunjid Ahmed")
    console.print("[bold yellow]GitHub:[/bold yellow] https://github.com/Sunjid-Ahmed")

    parser.add_argument("-i", "--ip", help="Target IP address", required=True)
    args = parser.parse_args()
    get_ip_info(args.ip)

if __name__ == "__main__":
    main()
