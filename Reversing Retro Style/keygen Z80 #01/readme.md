# keygenme Z80 #01

## Introduction

I was curious to know how some old forgotten software hand coded in z80 checked the keys. The following reverse engineering is for academic purposes only so some bytes are obscured to leave the scheme protected. Previous knowledge of z80 is assumed.

## Key check routine

The key check routine is easily found by inspecting the code that prints error, fail or success messages about the key check. Here it is:

```
register_key:
    push    hl
    ; check key length is exactly 10
    cp      10
    jr      nz, printKeyWrongLength
    ; copy key + null byte
    ld      de, key
    ld      hl, (word_key_ptr)
    ld      bc, 11
    ldir
    ; copy unique machine ID (5 bytes) by system call to know location in RAM
    call    getUniqueMachineId
    ; set flag to mark we are registering for the first time
    set     0, (iy+flag_o1)
    ; returns c set in case of success, nc otherwise
    call    checkKeyProper
    ; in case of fail print incorrect key and abort
    jr      nc, printKeyIncorrect
    pop     hl
    ret
```

Already we see that the key consist of 10 bytes.
The checkKeyProper is also called in another place, probably when starting the application.

```
test_key:
    call    sub_XXXX            ; system call to check something
    ret     nc
    ld      hl, key
    call    getUniqueMachineId
    res     0, (iy+flag_o1)
    jp      checkKeyProper
```

So getUniqueMachineId must be called before checkKeyProper. The only thing needed to know of getUniqueMachineId is that it gets 5 unique bytes per computer into temp4.

Moving on to the interesting part.

```
checkKeyProper:
    call    permuteBytes
    ld      hl, temp4
    ld      de, temp3
    ld      bc, 5
    ldir
    ld      hl, keyP
    ld      bc, 3
    ldir
    ld      hl, temp3
    ld      b, 64
    ld      de, table_permutation_1
    call    permute_buffer_bits
    call    checksum33
    ld      hl, temp1
    ld      b, 24
    ld      de, table_permutation_2
    call    permute_buffer_bits
    ld      hl, temp1+2
    set     0, (hl)
    call    decimal_to_int
    ld      hl, temp1+3
    ld      b, 24
    ld      de, table_permutation_3
    call    permute_buffer_bits
    ld      hl, temp1+3
    ld      de, temp1
    ld      b, 0
    call    add_ihl_ide_b_i
    call    add_ihl_ide_b_i
    call    add_ihl_ide_b_i
    ld      a, b
    cp      156
    jp      nz, check_key_fail
    ld      hl, temp1
    ld      b, 24
    ld      de, table_permutation_4
    call    permute_buffer_bits
    ld      hl, temp1
    ld      de, temp1_cpy
    ldi
    ldi
    ldi
    ld      a, (temp1_cpy)
    ld      hl, temp1_cpy+1
    add     a, (hl)
    inc     hl
    add     a, (hl)
    cp      6
    jp      nz, check_key_fail
    push    hl
    set     3, (flag_o2)               ; some other flag
    bit     0, (iy+flag_o1)            ; check if flag first time registering
    jr      z, check_key_success
    ld      hl, (word_key_ptr)         ; if not print something
    ld      a, 0Dh
    ld      bc, 10Ch
    call    som_XXXX                   ; something
    ld      hl, str_XXXX               ; some string
    call    prt_XXXX                   ; print
check_key_success:
    pop     bc
    scf                                ; success return carry set
    ret
check_key_fail:
    or      a                          ; success return carry reset
    ret


permuteBytes:
    ld      hl, key
    ld      de,  keyP+9
    ldi
    ld      de,  keyP+4
    ldi
    dec     de
    dec     de
    ldi
    dec     de
    dec     de
    dec     de
    dec     de
    ldi
    ldi
    inc     hl
    inc     hl
    ldi
    dec     hl
    dec     hl
    dec     hl
    ld      de,  keyP+8
    ldi
    dec     de
    dec     de
    ldi
    dec     de
    inc     hl
    dec     de
    dec     de
    ldi
    ldi
    ret


permute_buffer_bits:
    push    bc
    push    hl
    srl     b
    srl     b
    srl     b
    ld      a, b
    ld      hl, temp2
clear_permute_buffer:
    ld      (hl), 0
    inc     hl
    djnz    clear_permute_buffer
    pop     hl
    pop     bc
    ld      c, a
    push    bc
    push    hl
    call    actual_permute_bits
    pop     hl
    pop     bc
    ld      b, 0
    ex      de, hl
    ld      hl, temp2
    ldir
    ret


decimal_to_int:
    ld      de,  keyP+3
    ld      b, 7
    xor     a
    ld      hl, 0
decimal_to_int_lloop:
    push    de
    add     hl, hl
    rla
    ld      c, a
    ld      d, h
    ld      e, l
    add     hl, hl
    rla
    add     hl, hl
    rla
    add     hl, de
    adc     a, c
    pop     de
    ld      c, a
    ld      a, (de)
    inc     de
    sub     30h ; '0'
    call    add_hl_a
    ld      a, c
    adc     a, 0
    djnz    decimal_to_int_lloop
    ld      (temp1_3), a
    ld      a, h
    ld      (temp1_4), a
    ld      a, l
    ld      (temp1_5), a
    ret



checksum33:
    xor     a
    ld      hl, 1505h
    ld      de, temp3
    ld      b, 8
checksum33_loop:
    push    de
    ld      c, a
    ld      d, h
    ld      e, l
    push    bc
    ld      b, 5
checksum33_loop_inner:
    add     hl, hl
    rla
    djnz    checksum33_loop_inne
    pop     bc
    add     hl, de
    adc     a, c
    pop     de
    ld      c, a
    ld      a, (de)
    call    add_hl_a
    ld      a, c
    adc     a, 0
    inc     de
    djnz    checksum33_loop
    ld      (temp1), a
    ld      (temp1_1), hl
    ret

add_ihl_ide_b_i:
    ld      a, (de)
    add     a, (hl)
    ld      (de), a
    add     a, b
    ld      b, a
    inc     de
    inc     hl
    ret


actual_permute_bits_loop:
    inc     de
    dec     b
    ret     z
    ld      a, b
    and     7
    jr      nz, actual_permute_bits
    inc     hl
actual_permute_bits:
    rl      (hl)
    jr      nc, actual_permute_bits_loop
    push    hl
    ld      hl, lut_bit_shift
    ld      a, (de)
    and     7
    call    add_hl_a
    ld      c, (hl)
    ld      hl, temp2
    ld      a, (de)
    srl     a
    srl     a
    srl     a
    call    add_hl_a
    ld      a, (hl)
    or      c
    ld      (hl), a
    pop     hl
    jr      actual_permute_bits_loop


lut_bit_shift:
    db  80h
    db  40h
    db  20h
    db  10h
    db    8
    db    4
    db    2
    db    1


add_hl_a:
    push    bc
    ld      b, 0
    ld      c, a
    add     hl, bc
    pop     bc
    ret
```

That took some time to figure out and properly label... All the disassembly can also be found in the *ck.z80* file.

We can see that the key's 10 bytes consists of ASCII 0-9. So here lies the transcript of my notes for figuring out the function step by step:

```
routine checkKeyProper:

  1. permute bytes of key to a copy keyP
  keyP[9] = key[0]
  keyP[4] = key[1]
  keyP[3] = key[2]
  keyP[0] = key[3]
  keyP[1] = key[4]
  keyP[2] = key[7]
  keyP[8] = key[5]
  keyP[7] = key[6]
  keyP[5] = key[8]
  keyP[6] = key[9]

  2. copy (machine_id)* to (temp3)* (5 bytes)

  3. copy (keyP)* to (temp3+5)* (3 bytes)

  4. permute 64 bits in temp3 according to table1

  5. checksum33 of temp3 8 bytes and save into uint24 in temp1

  function checksum33()
    AHL = 0x001505  // 24 bit acumulator
    //temp3 is input
    for i from 0 to 7 step 1
      AHL = AHL * 33 + temp3[i]
    temp1[0] = AHL >> 16
    temp1[1] = AHL & 0x00F         // little endian
    temp1[2] = (AHL & 0x0F0) >> 8

  6. permute 24 bits of temp1 according to table2

  7. temp1[2] = temp1[2] | 0x01

  8. convert 7 chars of keyP[3]...keyP[9] to uint24 in temp1+3,
      interpreting the chars as ASCII decimal
      and not in little endian!
      temp1[3] = A
      temp1[4] = H
      temp1[5] = L

  9. permute 24 bits of temp1+3 according to table3

  10. sum of temp1 and temp1+3 mod 256 and modifications in temp1

  b = 0 // 8bit acumulator
  for i from 0 to 2 step 1
    b += (temp1[i] + temp1[i+3]) % 256
    temp1[i] = (temp1[i] + temp1[i+3]) % 256 // temp1 modified

  11. previous sum must be 156 or fail

  12. permute temp1 according to table4

  13. sum the 3 bytes of temp1 mod 256

  a = (temp1[0] + temp1[1] + temp1[2]) % 256

  14. previous sum must be 6 or fail

  15. key is valid

// permutation tables format
// table as number of bytes equal to the number of bits to permutate
each byte indicates that the n-th bit goes position table[n] in bits
```

The remaining dissassembly relevant to key check deals with creating a username string that contains the machine id in a hexadecimal like code slightly obfuscated with xor operation (note that this operation is reversible). See createUsername for reference. This username string was used to send to developer for him to generate a valid key for a that computer hardware ID.

## Key generator

So this looks simple enough that brute force should do it. So I implementated in C, following precisely the note above. It found several keys passing the check under a second! I tested and worked. Neat.

The C source code is found in the *keygen* folder. Beware bugs, it was made for working once. Decoding the username into the machine id is left unimplemented. Making a valid key from working backwards on the conditions could be interesting.

## Conclusion

The scheme consists of adding, bit shuffling, oring, xoring around and check for certain equalities. Username string is hex digits in disguise and key is a decimal number with 10 digits. No obfuscation tricks or brute forcing resistance found but what did I expect from an old z80 software.

## Afterword

I found this key scheme reused in other software from the same developer with different constants (bit permutation tables and equality test). Message me interesting 6502, 6800, 8080, 8086, Z80 and M68K obsolete software (no games) for retro computers with protection schemes for preservation. Thanks for reading.
