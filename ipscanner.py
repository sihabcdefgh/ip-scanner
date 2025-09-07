#!/usr/bin/env python3
import socket
import argparse
import ipaddress

def scan_port(ip, port, protocol="tcp"):
    try:
        if protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    sock.send(b"\r\n")
                    banner = sock.recv(1024).decode().strip()
                    if banner:
                        print(f"{port} open         {banner}")
                    else:
                        print(f"{port} open")
                except:
                    print(f"{port} open")
            sock.close()
        elif protocol == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(b"\r\n", (ip, port))
            try:
                data, _ = sock.recvfrom(1024)
                print(f"{port} open | Response: {data.decode().strip()}")
            except socket.timeout:
                print(f"[?] UDP {port} open|filtered (no response)")
            sock.close()
    except Exception:
        pass

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(","):
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def main():
    parser = argparse.ArgumentParser(description="Simple TCP/UDP Port Scanner with Service Banner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("-u", "--udp", action="store_true", help="Scan UDP ports instead of TCP")
    parser.add_argument("-p", "--ports", help="Specify ports")
    args = parser.parse_args()

    try:
        ip = str(ipaddress.ip_address(args.ip))
    except ValueError:
        print("Invalid IP address")
        return

    if args.ports:
        ports = parse_ports(args.ports)
    else:
        ports = range(1, 1000)

    protocol = "udp" if args.udp else "tcp"

    print(f"Scanning {ip} ({protocol.upper()})")
    for port in ports:
        scan_port(ip, port, protocol)

if __name__ == "__main__":
    main()
