import socket
from datetime import datetime

INPUT_FILE = "domains.txt"
OUTPUT_FILE = "resolved_ips.txt"


def read_domains(filename):
    """Read domain list from file, skipping comments and blanks."""
    try:
        with open(filename, "r") as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return domains
    except FileNotFoundError:
        print(f"⚠️ No {filename} found — nothing to resolve.")
        return []


def resolve_domain(domain):
    """Resolve a single domain to IPv4 and IPv6 addresses, add CIDR notation."""
    try:
        infos = socket.getaddrinfo(domain, None)
        ips = set()
        for info in infos:
            family, _, _, _, sockaddr = info
            ip = sockaddr[0]
            if family == socket.AF_INET:
                ips.add(f"{ip}/32")
            elif family == socket.AF_INET6:
                ips.add(f"{ip}/128")
        return list(ips)
    except Exception as e:
        print(f"❌ Failed to resolve {domain}: {e}")
        return []


def save_ips(ips, filename):
    """Save sorted unique IPs to file."""
    unique_ips = sorted(set(ips))
    with open(filename, "w") as f:
        for ip in unique_ips:
            f.write(ip + "\n")
    print(f"✅ Saved {len(unique_ips)} unique IPs to {filename}")


def main():
    print(f"🚀 Starting domain resolution at {datetime.utcnow().isoformat()}Z")
    domains = read_domains(INPUT_FILE)
    if not domains:
        print("⚠️ No domains to resolve.")
        return

    resolved_ips = []
    for domain in domains:
        ips = resolve_domain(domain)
        if ips:
            print(f"🌐 {domain} → {', '.join(ips)}")
            resolved_ips.extend(ips)

    if resolved_ips:
        save_ips(resolved_ips, OUTPUT_FILE)
    else:
        print("⚠️ No domains resolved successfully.")

    print("✅ Domain resolution completed.")


if __name__ == "__main__":
    main()
