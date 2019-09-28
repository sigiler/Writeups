
#include "utils.h"

void print_hex(uint8_t *bytes, int n_bytes) {
	char* str = malloc((n_bytes*2 + 2) * sizeof(char));
	char* hex_char = "0123456789ABCDEF";
	int i;
	for (i = 0; i < n_bytes; i++) {
		str[2*i] = hex_char[(bytes[i] & 0xFF) / 16];
		str[2*i+1] = hex_char[(bytes[i] & 0xFF) % 16];
	}
	str[2*i] = '\n';
	str[2*i+1] = 0;
	printf(str);
	free(str);
}

int random_int(int min, int max) {
   return min + rand() / (RAND_MAX / (max - min + 1) + 1);
}
