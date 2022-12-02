#!/usr/bin/env python3
import hashlib
import sys
import binascii
import struct

fname = sys.argv[1]

# https://www.quickprogrammingtips.com/python/how-to-calculate-md5-hash-of-a-file-in-python.html
hash5 = hashlib.md5()
hash256 = hashlib.sha256()
with open(fname,"rb") as f:
    for block in iter(lambda: f.read(4096),b""):
        hash5.update(block)
        hash256.update(block)

#https://stackoverflow.com/questions/46109815/convert-string-from-big-endian-to-little-endian-or-vice-versa-in-python
def int2bytes(i, enc):
    return i.to_bytes((i.bit_length() + 7) // 8, enc)
def convert_hex(str, enc1, enc2):
    return int2bytes(int.from_bytes(bytes.fromhex(str), enc1), enc2).hex()
def pad(strPad):
    while len(strPad) < 16:
        strPad = strPad + '0'
    return strPad

# hex5 = hash5.hexdigest()
# file5 = open('MD5-'+fname+'.txt', "w")
# file5.write(hex5)
# file5.close()

# hex256 = hash256.hexdigest()
# file256 = open('SHA-256-'+fname+'.txt', "w")
# file256.write(hex256)
# file256.close()

# https://books.google.com/books?id=7O-cBAAAQBAJ&pg=PA24&lpg=PA24&dq=struct.unpack(%27%3CI%27,+mbr%5B0x1C6:0x1CA%5D)&source=bl&ots=wx-EIkYjVZ&sig=ACfU3U0OoIY62DO-dVFaBtyVyfzZRmdMZA&hl=en&sa=X&ved=2ahUKEwjB6q_tnNz6AhU1LkQIHSFxD9kQ6AF6BAgIEAM#v=onepage&q&f=false
mbr = bytearray() 
try:
    bfile = open(fname, 'rb')
finally:
    mbr = bfile.read() 

partitions = []

# loop through all of the partitions and format the data
# for i in range(4):

enderecoS = 0x248
hexprtStart = mbr[enderecoS:0x250].hex()
addrPartitionTable = int(convert_hex(hexprtStart, 'big', 'little'), base=16) * 0x200

print("The start address for the partition table is: ", addrPartitionTable)
print("")

for i in range(128):
# for i in range(128):

    bytesForStartAddr = mbr[((addrPartitionTable + 0x20) + (i* 0x80)) : ((addrPartitionTable + 0x28) + (i* 0x80))].hex()
    bytesForEndAddr =  mbr[((addrPartitionTable + 0x28) + (i* 0x80)) : ((addrPartitionTable + 0x30) + (i* 0x80))].hex()
    
    bytesForStartAddr = convert_hex(bytesForStartAddr, 'big', 'little')
    bytesForEndAddr = convert_hex(bytesForEndAddr, 'big', 'little')

    bytesForStartAddr = pad(bytesForStartAddr)
    bytesForEndAddr = pad(bytesForEndAddr)
    
    print("The start address for partition "+str(i+1)+" is: 0x", bytesForStartAddr)
    print("The end address for partition "+str(i+1)+" is: 0x", bytesForEndAddr)
    print("")

