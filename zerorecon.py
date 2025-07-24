from pathlib import Path

# Creating the ZeroRecon Python script, terminal-compatible
zerorecon_code = '''
# ZeroRecon - Full Scope OSINT & Recon Tool
# Developed by KRISHNA

import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime

BANNER = """
███████╗███████╗██████╗  ██████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║
███████╗█████╗  ██████╔╝██║   ██║██████╔╝█████╗  ██║   ██║██╔██╗ ██║
╚════██║██╔══╝  ██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝  ██║   ██║██║╚██╗██║
███████║███████╗██║     ╚██████╔╝██║     ███████╗╚██████╔╝██║ ╚████║
╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
            FULL-SCOPE OSINT TOOL by KRISHNA ⚔️
"""

print(BANNER)
domain = input("Enter target domain (e.g. example.com): ").strip()

out_dir = f"zerorecon_reports/{domain}"
os.makedirs(out_dir, exist_ok=True)
report_txt = os.path.join(out_dir, "recon_output.txt")

def write_log(text):
    with open(report_txt, "a") as f:
        f.write(text + "\\n")
    print(text)

write_log(f"[+] Target: {domain}")
write_log(f"[+] Scan Time: {datetime.now()}\\n")

# 1. Subdomain Enumeration via crt.sh
def get_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return []
        json_data = res.json()
        subdomains = set()
        for entry in json_data:
            name = entry.get("name_value", "")
            for sub in name.split("\\n"):
                if domain in sub:
                    subdomains.add(sub.strip())
        return sorted(list(subdomains))
    except Exception as e:
        return []

write_log("[*] Gathering Subdomains from crt.sh ...")
subs = get_subdomains(domain)
write_log(f"[+] Found {len(subs)} subdomains")
for s in subs:
    write_log(" - " + s)

# 2. Top Port Check
write_log("\\n[*] Checking common ports ...")
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
import socket
for port in common_ports:
    sock = socket.socket()
    sock.settimeout(1)
    try:
        sock.connect((domain, port))
        write_log(f"[+] Port {port} is OPEN")
    except:
        pass
    sock.close()

# 3. Wayback URLs
write_log("\\n[*] Fetching Wayback Machine URLs ...")
wayback_url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey"
try:
    resp = requests.get(wayback_url, timeout=10)
    urls = list(set(resp.text.strip().split("\\n")))
    write_log(f"[+] {len(urls)} URLs found in Wayback Machine")
    for u in urls[:10]:
        write_log(" - " + u)
except:
    write_log("[!] Failed to fetch Wayback URLs")

# 4. Extract title
write_log("\\n[*] Getting Web Title ...")
try:
    r = requests.get("http://" + domain, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title else "No Title"
    write_log(f"[+] Web Title: {title}")
except:
    write_log("[!] Failed to retrieve title")

# 5. Save Report as PDF
write_log("\\n[✔] Generating PDF Report ...")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, open(report_txt).read())
pdf.output(os.path.join(out_dir, "report.pdf"))
write_log("[✔] Report saved at: " + os.path.join(out_dir, "report.pdf"))
print("\\n[✓] Scan Complete. Stay Sharp ⚔️")
'''

# Save the script
output_path = Path("/mnt/data/zerorecon.py")
with open(output_path, "w") as f:
    f.write(zerorecon_code)

output_path
