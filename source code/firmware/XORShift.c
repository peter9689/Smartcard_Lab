#include <stdint.h>
#include <stdlib.h>

static uint8_t a=0;
static uint8_t seednow=0xaa;

void XORSHIFTseed(uint8_t seed) {
	seednow= seed;
}

uint8_t XORSHIFTout()
{
        seednow^=seednow<<3;
        seednow^=seednow>>5;
        seednow^=a++>>2;
        return seednow;
}