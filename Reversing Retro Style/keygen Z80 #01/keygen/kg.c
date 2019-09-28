
#include "kg.h"

// optional, we could obtain dev_id directly
uint8_t* username_to_dev_id(uint8_t *username) {
	uint8_t *dev_id = (uint8_t*) malloc(6 * sizeof(uint8_t));

	// TODO implement

	return dev_id;
}

// optional if we code the the key gen in the device or ask the user to obtain the dev_id for us
uint8_t* key_gen_from_username(uint8_t* username) {
	uint8_t *dev_id = username_to_dev_id(username);
	uint8_t* key = key_gen_from_dev_id(dev_id);
	free(dev_id);
	return key;
}

uint8_t* key_gen_from_dev_id(uint8_t* dev_id) {

	// key must consist of 10 decimal digits only
	uint8_t* key = (uint8_t*) malloc(10 * sizeof(uint8_t));
	char *valid_char = "0123456789";

	// TODO non brute force keygen

	int pos[10] = {0};
	int pos_len = 10;
	int index_max = 10;
	int i;
	int end = 0;

	while (!end) {
		// copy key
		for (i = 0; i < pos_len; i++) {
			key[i] = valid_char[pos[i]];
		}
		// test key
		if (check_key(dev_id, key)) {
			return key;
		}
		// end cond
		end = 1;
		for (i = 0; i < pos_len; i++) {
			if (pos[i] < index_max) {
				end = 0;
				break;
			}
		}
		// step pos
		for (i = 0; i < pos_len; i++) {
			if (pos[i] < index_max) {
				pos[i] += 1;
				break;
			} else {
				pos[i] = 0;
			}
		}
	}

	return key;
}
