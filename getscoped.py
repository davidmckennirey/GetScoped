import ipaddress
import argparse
import json
from typing import List

def perror(msg: str):
    print(f"[!] ERROR - {msg}")

def pinfo(msg: str):
    print(f"[*] {msg}")

def check_in_scope(ip_addr: str, scope: List) -> bool:
    """Return true if the provided IP address is in scope or false otherwise"""
    ip = ipaddress.ip_address(ip_addr)
    for ip_network in scope:
        if ip in ip_network:
            return True
    return False

def dump_to_file(hosts: List, filename: str):
    with open(filename, "w") as f:
        for host in hosts:
            f.write(f"{host.get('host')} [{host.get('ip')}]\n")

def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scope", help="Scope file containing CIDRs and/or IP addresses", required=True)
    parser.add_argument("-d", "--dnsx", help="JSON output file from dnsx", required=True)
    parser.add_argument("-oI", "--output-in", help="Output for in-scope hosts (default='in-scope.txt')", default="in-scope.txt")
    parser.add_argument("-oO", "--output-out", help="Output for out-of-scope hosts (default='out-of-scope.txt')", default="out-of-scope.txt")
    return parser.parse_args()

def main():
    args = cli()
    scope = []
    dnsx = []
    in_scope = []
    out_of_scope = []

    # Read in scope as ip_networks
    try:
        with open(args.scope) as f:
            for line in f:
                scope.append(ipaddress.ip_network(line.strip(), strict=False))
    except FileNotFoundError:
        perror(f"Could not open scope file: {args.scope}")
        exit(0)
    pinfo(f"Successfully read in scope file: {args.scope}")

    # Read in dnsx output
    try:
        with open(args.dnsx) as f:
            for line in f:
                dnsx.append(json.loads(line))
    except FileNotFoundError:
        perror(f"Could not open dnsx output file: {args.scope}")
        exit(0)    
    pinfo(f"Successfully read in dnsx output file: {args.dnsx}")

    # Check if each host in dnsx is in scope or not
    for host in dnsx:
        ip_list = host.get('a', [])
        if ip_list:
            for ip in ip_list:
                if check_in_scope(ip, scope):
                    in_scope.append({
                        "host": host.get('host'),
                        "ip": ip
                    }) 
                else:
                    out_of_scope.append({
                        "host": host.get('host'),
                        "ip": ip
                    })
    pinfo(f"Successfully checked scope, dumping to output files: {args.output_in} and {args.output_out}")

    # output scope files
    dump_to_file(out_of_scope, args.output_out)

    dump_to_file(in_scope, args.output_in)
    pinfo("Done, happy hunting!")


if __name__ == "__main__":
    main()