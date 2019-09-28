
#include "common.h"
#include "utils.h"
#include "ck.h"
#include "kg.h"

int main(void) {
	printf("start\n");

	int valid;
	uint8_t dev_id_test[6] = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC};  // lies
	uint8_t key_test[10] = "0123456789";
	uint8_t *username_code;

	//FIXME strings may not null terminated...

	username_code = create_username(dev_id_test);
	printf("username_code = %s\n", username_code);

	valid = check_key(dev_id_test, key_test);
	if (valid) {
		printf("key passed\n");
	} else {
		printf("key failed\n");
	}

	uint8_t *key_gen = key_gen_from_dev_id(dev_id_test);
	printf("key generated = %s\n", key_gen);
	valid = check_key(dev_id_test, key_gen);
	if (valid) {
		printf("is valid\n");
	} else {
		printf("is invalid\n");
	}

	// clean up
	free(username_code);
	free(key_gen);

	printf("finish\n");
	return EXIT_SUCCESS;
}
