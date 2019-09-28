
# primepwn

Analyzing the binary in IDA, the decompiled code is

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  test_prime();
  return 0;
}

__int64 test_prime()
{
  unsigned int iterator; // [rsp+Ch] [rbp-14h]
  size_t len; // [rsp+18h] [rbp-8h]

  if ( mmap((void *)0x1337000, 0x1000uLL, 7, 50, -1, 0LL) != (void *)0x1337000 )
  {
    perror("error on mmap");
    exit(1);
  }
  len = fread((void *)0x1337000, 1uLL, 0x1000uLL, _bss_start);
  for ( iterator = 0; (signed int)iterator < len; ++iterator )
  {
    if ( !(unsigned __int8)is_prime(*(_BYTE *)((signed int)iterator + 0x1337000LL)) )
    {
      printf("Byte %d (value: %u) is not prime.\n", iterator, *(unsigned __int8 *)((signed int)iterator + 0x1337000LL));
      exit(0);
    }
  }
  puts("All bytes are prime!");
  return jump_to((__int64 (*)(void))0x1337000);
}


signed __int64 __fastcall is_prime(unsigned __int8 a1)
{
  signed int i; // [rsp+10h] [rbp-4h]

  if ( a1 <= 1u )
    return 0LL;
  for ( i = 2; i <= 255 && a1 > i; ++i )
  {
    if ( !(a1 % i) )
      return 0LL;
  }
  return 1LL;
}
```

This program allocates 4 KiB in 0x1337000 address with all permissions (read, write, execute),
then copies the same length from stdin to there with the restriction that every byte must be a prime number
and jumps there.

The idea is to craft shellcode using only prime bytes opcodes. We can use self modifying code.

After coding a script in python using pwntools that prints some valid opcodes,
we find these opcodes of interest that are enough to insert our shellcode

```
add eax,imm32
sbb  eax,imm32
mov  DWORD PTR [rdi],eax
mov  ecx,eax
mov  eax,edi
mov  edi,eax
mov  eax,ecx
```

Looking at the disassembly before the jumpTo, we note that rax == 0x1337000 and rdi == 0x1337000.
Using the fact that any number from 4 to 254 is the sum of two primes (Goldbach conjecture),
dealing with the special cases (1 and 255 found in the shellcode), finally
 we can put any byte we need into memory.

The pseudo code is
```
add edi,offset
add eax,a[i]
add eax,b[i]
mov DWORD PTR [rdi],eax  % a[i] + b[i] == shellcode[i]
add edi,1
% ...
% repeat for each byte in shellcode
% ...
offset:
	% shellcode got here by SMC
```

Remark 1: the upper 32 bits of rax and rdi are 0, so there are no worries in doing 32 bit arithmetic that clears those upper bits as side effect

Remark 2: sbb was used for the special cases (1 and 255)

Remark 3: add overflowing the lsb was also used

Remark 4: payload must fit in 4 KiB, it fit first try

Remark 5: assembly != machine code, some mnemonics can assemble to various opcode encodings (sometimes not even the same length and timing) and the pwntools assembler did not do what we wanted so we manually inserted the machine code

We automatize the task as can be seen in the python script and getting us a shell to "cat flag".

The final payload can be inspected using the commented prints.
You can run locally for a demonstration.
