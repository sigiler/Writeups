
#ifndef CK_H_
#define CK_H_

#include "common.h"

uint8_t convert_to_userchar(uint8_t a, int *c);
uint8_t* create_username(uint8_t *dev_id);
uint8_t* permute(uint8_t* bits, uint8_t* permutation, int n_bits);
void checksum33(uint8_t *mem_3, uint8_t *mem_O);
void readKeyDec(uint8_t* ascii_numbers, uint8_t *mem_O);
int check_key(uint8_t *dev_id, uint8_t* key);


#endif /* CK_H_ */
