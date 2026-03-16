#!/usr/bin/env python3
"""cidrlist - Expand CIDR ranges, check membership, merge subnets."""
import argparse, ipaddress, sys

def main():
    p = argparse.ArgumentParser(description='CIDR range utility')
    sub = p.add_subparsers(dest='cmd')

    exp = sub.add_parser('expand', help='List all IPs in CIDR')
    exp.add_argument('cidr')
    exp.add_argument('--no-network', action='store_true', help='Exclude network/broadcast')

    chk = sub.add_parser('contains', help='Check if IP is in CIDR')
    chk.add_argument('cidr')
    chk.add_argument('ip')

    inf = sub.add_parser('info', help='CIDR info')
    inf.add_argument('cidr')

    mrg = sub.add_parser('merge', help='Merge overlapping CIDRs')
    mrg.add_argument('cidrs', nargs='+')

    spl = sub.add_parser('split', help='Split CIDR into smaller prefixes')
    spl.add_argument('cidr')
    spl.add_argument('prefix', type=int, help='New prefix length')

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); return

    if args.cmd == 'expand':
        net = ipaddress.ip_network(args.cidr, strict=False)
        hosts = net.hosts() if args.no_network else net
        for ip in hosts:
            print(ip)
    elif args.cmd == 'contains':
        net = ipaddress.ip_network(args.cidr, strict=False)
        ip = ipaddress.ip_address(args.ip)
        result = ip in net
        print(f"{args.ip} {'is' if result else 'is NOT'} in {net}")
        sys.exit(0 if result else 1)
    elif args.cmd == 'info':
        net = ipaddress.ip_network(args.cidr, strict=False)
        print(f"Network:   {net.network_address}")
        print(f"Broadcast: {net.broadcast_address}")
        print(f"Netmask:   {net.netmask}")
        print(f"Hostmask:  {net.hostmask}")
        print(f"Hosts:     {net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses}")
        print(f"Prefix:    /{net.prefixlen}")
        print(f"Version:   IPv{net.version}")
        print(f"Private:   {net.is_private}")
    elif args.cmd == 'merge':
        nets = [ipaddress.ip_network(c, strict=False) for c in args.cidrs]
        for net in ipaddress.collapse_addresses(nets):
            print(net)
    elif args.cmd == 'split':
        net = ipaddress.ip_network(args.cidr, strict=False)
        for subnet in net.subnets(new_prefix=args.prefix):
            print(subnet)

if __name__ == '__main__':
    main()
