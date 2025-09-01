import ipaddress
import os
import socket
import struct
import sys
import threading
import time

SUBNET = '192.168.0.0/24'
MESSAGE = 'PYTHONRULES!'

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff[:8])
        self.type = header[0]
        self.code = header[1]
        self.checksum = header[2]
        self.id = header[3]
        self.seq = header[4]

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            time.sleep(0.05)
            sender.sendto(MESSAGE.encode(), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f"{str(self.host)} *"])
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol_num == 1:
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.ip_network(SUBNET):
                            if raw_buffer[-len(MESSAGE):] == MESSAGE.encode():
                                hosts_up.add(str(ip_header.src_address))
                                print(f"Host Up: {ip_header.src_address}")
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print('\n')
            print(f"Summary: Hosts up on {SUBNET}")
            for host in sorted(hosts_up):
                print(host)
            print('')

def main():
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.219.105'
    s = Scanner(host)
    time.sleep(2)
    t = threading.Thread(target=udp_sender, daemon=True)
    t.start()
    s.sniff()

if __name__ == '__main__':
    main()