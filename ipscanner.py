#!/usr/bin/env python3
import socket
import argparse
import threading

def tcp_scan(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[TCP] Port {port} OPEN")
        s.close()
    except Exception:
        pass

def udp_scan(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto(b"Hello", (target, port))
        try:
            data, _ = s.recvfrom(1024)
            print(f"[UDP] Port {port} OPEN (response: {data})")
        except socket.timeout:
            print(f"[UDP] Port {port} OPEN|FILTERED (no response)")
        s.close()
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Simple TCP/UDP Port Scanner")
    parser.add_argument("target", help="Target IP/domain")
    parser.add_argument("-u", "--udp", action="store_true", help="Scan UDP Ports")
    args = parser.parse_args()

    target = args.target
    start_port, end_port = 1, 1000   # default range

    threads = []
    print(f"Scanning {target} pada port {start_port}-{end_port}...\n")

    for port in range(start_port, end_port + 1):
        t_tcp = threading.Thread(target=tcp_scan, args=(target, port))
        threads.append(t_tcp)
        t_tcp.start()

        if args.udp:
            t_udp = threading.Thread(target=udp_scan, args=(target, port))
            threads.append(t_udp)
            t_udp.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()