
#include "utils.h"
#include "ck.h"

uint8_t convert_to_userchar(uint8_t a, int *c) {

	char* table = "abcdefghijklmnop";  // shush

	a = (a ^ *c) & 0xFF;
	*c = a; // c modified
	*c = ((*c << 1) & 0x0F) | ((*c >> 3) & 0x01); // rotate left the lower 4 bits of c

	return (uint8_t) table[a];
}

uint8_t* create_username(uint8_t *dev_id) {

	uint8_t *username = (uint8_t *) malloc(12 * sizeof(uint8_t));

	// modified in convert with xor
	int c = 0; // 8bit

	// do a sum and put into the last byte
	int a = 0; // 8bit accumulator
	int i;
	for (i = 0; i < 5; i++) {
		a = (a << 1) & 0xFF;
		a = (a + dev_id[i]) & 0xFF;
	}
	dev_id[5] = a;

	// convert the 6 bytes into ASCII string
	for (i = 0; i < 6; i++) {
		username[2*i] = convert_to_userchar(dev_id[5-i] & 0x0F, &c);
		username[2*i+1] = convert_to_userchar(dev_id[5-i] >> 4, &c);
	}

	return username;
}


uint8_t* permute(uint8_t* bits, uint8_t* permutation, int n_bits) {

	int i, src_bit, src_byte, dest_bit, dest_byte;
	uint8_t mask_src, mask_dest;
	int n_bytes = n_bits / 8;
	uint8_t *new_bits = malloc(n_bytes);

	// reset new_bits
	for (i = 0; i < n_bytes; i++) {
		new_bits[i] = 0;
	}

	// send one bit each time to destination
	for (i = 0; i < n_bits; i++) {
		src_bit = i % 8;
		src_byte = i / 8;
		dest_bit = permutation[i] % 8;
		dest_byte = permutation[i] / 8;
		mask_src = 0x80 >> src_bit;
		if (bits[src_byte] & mask_src) {
			mask_dest = 0x80 >> dest_bit;
			new_bits[dest_byte] |= mask_dest;
		}
	}

	// copy back to bits
	for (i = 0; i < n_bytes; i++) {
		bits[i] = new_bits[i];
	}
	free(new_bits);

	return bits;
}

void checksum33(uint8_t *OPi, uint8_t *mem_tmp) {
	/*
	int AHL = 0x001505; // 24 bit accumulator
	int i;
	for (i = 0; i < 8; i++) {
		AHL = (AHL*33) & 0xFFFFFF;  // assuming no overflow, this overflow is complicated
		AHL = (AHL + OPi[i]) & 0xFFFFFF;
	}
	OPtmp[0] = (AHL & 0xFF0000) >> 16;
	OPtmp[1] = (AHL & 0x0000FF); // little endian
	OPtmp[2] = (AHL & 0x00FF00) >> 8;
	*/

	int A = 0; // 8 bit accumulator
	int HL = 0x1505; // 16 bit accumulator
	int C = 0;  // 8 bit temp
	int DE = 0; // 16 bit temp
	int cf = 0; // 1 bit carry flag
	int i, j;
	for (i = 0; i < 8; i++) {
		C = A;
		DE = HL;
		for (j = 0; j < 5; j++) {
			cf = (HL >> 15) & 0x01;
			HL = (HL + HL) & 0xFFFF; // add hl,hl
			A = ((A << 1) & 0xFF) | cf; // rla, cf discarded so no need to compute
		}
		cf = ((HL + DE) > 0xFFFF);
		HL = (HL + DE) & 0xFFFF; // add hl,de
		A = (A + C + cf) & 0xFF; // adc a,c

		cf = ((HL + OPi[i]) > 0xFFFF);
		HL = (HL + OPi[i]) & 0xFFFF; // "add hl,(OP1)"
		A = (A + cf) & 0xFF; // adc a,0
	}
	mem_tmp[0] = A;
	mem_tmp[1] = (HL & 0xFF);  // little endian
	mem_tmp[2] = (HL >> 8);

}

void readKeyDec(uint8_t* OPi, uint8_t *OPtmp) {
	/*
	int AHL = 0;
	int i;
	for (i = 0; i < 7; i++) {
		AHL = (AHL * 10) & 0xFFFFFF;  // assuming no overflow, this overflow is complicated
		AHL = (AHL + OPi[i] - 0x30) & 0xFFFFFF;
	}
	OPtmp[3] = (AHL & 0xFF0000) >> 16;
	OPtmp[4] = (AHL & 0x00FF00) >> 8;  // odd but indeed it is not little endian here, double checked the dissassembly
	OPtmp[5] = (AHL & 0x0000FF);
	*/
	int A = 0;
	int HL = 0;
	int C = 0;
	int DE = 0;
	int cf = 0;
	int i;
	for (i = 0; i < 7; i++) {
		cf = (HL >> 15) & 0x01;
		HL = (HL + HL) & 0xFFFF; // add hl,hl
		A = ((A << 1) & 0xFF) | cf; // rla

		C = A;
		DE = HL;

		cf = (HL >> 15) & 0x01;
		HL = (HL + HL) & 0xFFFF; // add hl,hl
		A = ((A << 1) & 0xFF) | cf; // rla

		cf = (HL >> 15) & 0x01;
		HL = (HL + HL) & 0xFFFF; // add hl,hl
		A = ((A << 1) & 0xFF) | cf; // rla

		cf = ((HL + DE) > 0xFFFF);
		HL = (HL + DE) & 0xFFFF; // add hl,de
		A = (A + C + cf) & 0xFF; // adc a,c

		cf = ((HL + OPi[i] - 0x30) > 0xFFFF);
		HL = (HL + OPi[i] - 0x30) & 0xFFFF; // "add hl,((OP1) - 0x30)"
		A = (A + cf) & 0xFF; // adc a,0

	}
	OPtmp[3] = A;
	OPtmp[4] = (HL >> 8);
	OPtmp[5] = (HL & 0xFF);
}


int check_key(uint8_t *dev_id, uint8_t *key) {

	// dev_id is 5 or 6 bytes (we only use the first 5 here)
	// key is 10 bytes of ascii decimal digits

	// memory used
	uint8_t keyP[10] = {0,0,0,0,0,0,0,0,0,0};
	uint8_t mem_3[8] = {0,0,0,0,0,0,0,0};
	uint8_t mem_1[8] = {0,0,0,0,0,0,0,0};

	// permute bytes
	keyP[9] = key[0];
	keyP[4] = key[1];
	keyP[3] = key[2];
	keyP[0] = key[3];
	keyP[1] = key[4];
	keyP[2] = key[7];
	keyP[8] = key[5];
	keyP[7] = key[6];
	keyP[5] = key[8];
	keyP[6] = key[9];

	int i;
	// copy 5 bytes of dev_id into OP3
	for (i=0; i < 5; i++) {
		mem_3[i] = dev_id[i];
	}

	// copy 3 bytes of ASCII decimal digits into OP3+5
	for (i=0; i < 3; i++) {
		mem_3[i+5] = keyP[i];
	}

	// permutation 1
	uint8_t table1[64] = {};  // shush

	permute(mem_3, table1, 64);

	// a checksum and modifies OP1
	checksum33(mem_3, mem_1);

	// permutation 2
	uint8_t table2[24] = {};  // shush
	permute(mem_1, table2, 24);

	// set this bit
	mem_1[2] |= 0x01;

	// convert 7 chars of keyP[3]...keyP[9] to uint24 in OP1[3],OP1[4],OP1[5]
	readKeyDec(&keyP[3], mem_1);

	// permutation 3
	uint8_t table3[] = {};  // shush
	permute(&mem_1[3], table3, 24);

	// check sum 1
	int b = 0; // 8 bit accumulator
	for (i = 0; i < 3; i++) {
		  b = (b + mem_1[i] + mem_1[i+3]) & 0xFF;
		  mem_1[i] = (mem_1[i] + mem_1[i+3]) & 0xFF;  // OP1 modified
	}

	int passed = 1;

	int bb = 156;
	if (b != bb) {
		passed = 0;
	}

	// permutation 4
	uint8_t table4[] = {};  // shush
	permute(mem_1, table4, 24);

	// check sum 2
	int a = 0;  // 8 bit accumulator
	for (i = 0; i < 3; i++) {
		a = (a + mem_1[i]) & 0xFF;
	}

	int aa = 6;
	if (a != aa) {
		return 0;
	}

	// valid key
	return passed;
}
