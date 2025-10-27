import socket

def get_ip_with_prefix(domain):
    try:
        info = socket.getaddrinfo(domain, None)
        ips = set()
        for result in info:
            ip = result[4][0]
            if ':' in ip:
                ips.add(f"{ip}/128")  # IPv6
            else:
                ips.add(f"{ip}/32")   # IPv4
        return list(ips)
    except socket.gaierror:
        return []

# Read domain list
with open("KETLED-DOMAIN-LIST.txt", "r") as f:
    domains = [line.strip() for line in f if line.strip()]

resolved_ips = set()

for domain in domains:
    resolved_ips.update(get_ip_with_prefix(domain))

# Write to file
with open("resolved_ips.txt", "w") as f:
    for ip in sorted(resolved_ips):
        f.write(ip + "\n")
