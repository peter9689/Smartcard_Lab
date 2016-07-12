#include <stdint.h>

#ifndef MT
	#include <stdlib.h>
#endif

#ifdef TRNG
	#include "adc.h"
#endif

#include "hiding.h"
#include "XORShift.h"

uint8_t seq1[4] = {0, 1, 2, 3};
uint8_t seq2[4] = {0, 1, 2, 3};

void numofnop(uint8_t a[])
{
    int i,sum = 0;
    uint32_t test=0;
		
    for(i=0; i<39; i++)
    {		
		#ifdef MT
			a[i] = XORSHIFTout() % 255;
		#else
			a[i] = rand() % 255;
        #endif
        sum += a[i];
    }
    a[39] = 40*150 -sum;
}
//nop operations
void nop_operations(uint8_t num)
{
    int i;
    for(i=0; i<num; i++)
    {
        asm("nop");
    }
}

void seq_random(uint8_t a[4])
{
    int i;
    int index;
    int temp;

    for (i = 3; i > 0; i--)
    {
		#ifdef MT
			index = XORSHIFTout() % i;
		#else
			index = rand() % i;
        #endif
        
        temp = a[i];
        a[i] = a[index];
        a[index] = temp;
    }
}
