from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

OUTDIR = '/root/Desktop/pictures'
PCAPS = '/root/Downloads'

Response = collections.namedtuple('Response', ['header', 'payload'])

def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+4]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    header = {}
    for line in header_raw.split(b'\r\n'):
        try:
            key, value = line.split(b': ', 1)
        except ValueError:
            continue
        header[key.decode().lower()] = value.decode()
    return header

class Recapper:
    def __init__(self, fname):
        pcap = rdpcap(fname)
        self.sessions = pcap.sessions()
        self.responses = []

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()
            if payload:
                header = get_header(payload)
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload))

    def write(self, content_type='image'):
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR)
        for i, response in enumerate(self.responses):
            try:
                headers, payload = response
                if 'content-type' not in headers:
                    continue
                if content_type not in headers['content-type']:
                    continue
                content, content_subtype = headers['content-type'].split('/')
                if 'content-encoding' in headers:
                    if headers['content-encoding'] == 'gzip':
                        payload = zlib.decompress(payload, zlib.MAX_WBITS | 16)
                    elif headers['content-encoding'] == 'deflate':
                        payload = zlib.decompress(payload)
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_subtype}')
                body = payload[payload.index(b'\r\n\r\n')+4:]
                with open(fname, 'wb') as f:
                    f.write(body)
                print(f"[*] Wrote {fname}")
            except Exception as e:
                print(f"[*] Failed to write file: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pcapfile')
    args = parser.parse_args()
    recapper = Recapper(args.pcapfile)
    recapper.get_responses()
    recapper.write('image')

if __name__ == '__main__':
    main()