#include <stdint.h>
#include "MersenneTwister.h"

static uint8_t s=0xaa,a=0;


uint8_t rnd(void) {
        s^=s<<3;
        s^=s>>5;
        s^=a++>>2;
        return s;
}

uint8_t seedRNG(uint8_t num)
{
	s = num;
}
