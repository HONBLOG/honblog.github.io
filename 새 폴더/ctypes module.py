from ctypes import *
import socket
import struct

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4), #no mark 4 bit char
        ("version", c_ubyte, 4), #no mark 4 bit char
        ("tos", c_ubyte, 8), # 1byte char
        ("len", c_ushort, 16), # 2byte no mark short
        ("id", c_ushort, 16), # 2byte no mark short
        ("offset", c_ushort, 16), # 2byte no mark short
        ("ttl", c_ubyte, 8), # 1byte char
        ("protocol_num", c_ubyte, 8), #1 byte char
        ("sum", c_ushort, 16), # no mark 2 byte shot
        ("src", c_uint32, 32), # no mark 4 byte int
        ("dst", c_uint32, 32) # no mark 4 byte int
        ]
def __new__(cls, socket_buffer=None):
    return cls.from_buffer_copy(socket_buffer)
def __init__(self, socket_buffer=None):
    #human readable IP
    self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
    self.src_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        