
#ifndef KG_H_
#define KG_H_

#include "common.h"
#include "ck.h"

uint8_t* username_to_dev_id(uint8_t *username);
uint8_t* key_gen_from_username(uint8_t* username);
uint8_t* key_gen_from_dev_id(uint8_t* dev_id);

#endif /* KG_H_ */
