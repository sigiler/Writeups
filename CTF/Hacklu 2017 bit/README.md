
#  bit (pwn)

The decompiled code is

```C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax@2
  __int64 v4; // rsi@5
  __int64 v5; // rax@5
  __int64 v6; // rsi@6
  __int64 v7; // [sp+1038h] [bp-8h]@1

  v7 = *MK_FP(__FS__, 40LL);
  if ( __isoc99_scanf(4196308LL, 6295576LL, 6295584LL) == 2 )
  {
    if ( (unsigned int)dword_601020 <= 7 )
    {
      mprotect((void *)(qword_601018 & 0xFFFFFFFFFFFF1000LL), 0x1000uLL, 7);
      v4 = qword_601018;
      v5 = qword_601018;
      *(_BYTE *)qword_601018 ^= 1 << dword_601020;
      *(_BYTE *)v4 = *(_BYTE *)v5;
      mprotect((void *)(qword_601018 & 0xFFFFFFFFFFFF1000LL), 0x1000uLL, 5);
      result = 0;
    }
    else
    {
      result = -1;
    }
  }
  else
  {
    result = -1;
  }
  v6 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

Basically it receives a string in the format 'address:bit_index',
 unlock the memory for writes, xor/flip one bit, locks memory again and returns.
In the dissassembly there is a stack protection check.

The plan is to make a loop back into main with self modifying code and 
 good targets are jumps, calls and the return address in the stack 
 if it passes the stack check.

After looking into the opcode hex codes, possible code intervals that goto
 main and coding find function in solve.py script, it finds us 
 the input "0x400714:5" that changes

```
0x400713      call _mprotect
```

into

```
0x400540       call    start
```

where start is

```
0x400540 start:
0x400540                 xor     ebp, ebp
0x400542                 mov     r9, rdx
0x400545                 pop     rsi
0x400546                 mov     rdx, rsp
0x400549                 and     rsp, 0FFFFFFFFFFFFFFF0h
0x40054D                 push    rax
0x40054E                 push    rsp
0x40054F                 mov     r8, offset nullsub_1
0x400556                 mov     rcx, offset loc_400740
0x40055D                 mov     rdi, offset main
0x400564                 call    ___libc_start_main
0x400569                 hlt
```

doing what we wanted. So now we automatize in solve.py sending all the
inputs for enabling the loop, bit flip the shellcode in memory after
the hijacked call, disable the loop to let the shell code run getting us the flag.
