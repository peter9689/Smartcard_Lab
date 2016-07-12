#include <stdint.h>
#include "masking.h"
#include "aes.h"

#ifndef MT
	#include <stdlib.h>
#endif

#ifdef TRNG
	#include "adc.h"
#endif

#ifdef MT
	#include "XORShift.h"
#endif


uint8_t mask_sub1, mask_sub2;
uint8_t mask1, mask2, mask3, mask4;
uint8_t mask11, mask22, mask33, mask44;
uint8_t rsbox_m[256] = {0};

uint8_t getSBox_mInvert(uint8_t num)
{
  return rsbox_m[num];
}

static uint8_t xtime(uint8_t x)
{
  return ((x<<1) ^ (((x>>7) & 1) * 0x1b));
}

// Multiply is used to multiply numbers in the field GF(2^8)
static uint8_t Multiply(uint8_t x, uint8_t y)
{
  return (((y & 1) * x) ^
       ((y>>1 & 1) * xtime(x)) ^
       ((y>>2 & 1) * xtime(xtime(x))) ^
       ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^
       ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))));
}


void ReMask(void)
{
    int i;
    for(i=0;i<4;++i)
  {
    (*state)[i][0] = (*state)[i][0]^mask11^mask_sub1;
    (*state)[i][1] = (*state)[i][1]^mask22^mask_sub1;
    (*state)[i][2] = (*state)[i][2]^mask33^mask_sub1;
    (*state)[i][3] = (*state)[i][3]^mask44^mask_sub1;
  }
}

void calcSBOX_m(void){
    for (int i=0;i<256;i++)
    {
        rsbox_m[i^mask_sub1] = getSBoxInvert(i)^mask_sub2;
    }
}

void InvMixColumns_mask(int a, int b, int c, int d)
{
    mask11 = Multiply(a, 0x0e) ^ Multiply(b, 0x0b) ^ Multiply(c, 0x0d) ^ Multiply(d, 0x09);
    mask22 = Multiply(a, 0x09) ^ Multiply(b, 0x0e) ^ Multiply(c, 0x0b) ^ Multiply(d, 0x0d);
    mask33 = Multiply(a, 0x0d) ^ Multiply(b, 0x09) ^ Multiply(c, 0x0e) ^ Multiply(d, 0x0b);
    mask44 = Multiply(a, 0x0b) ^ Multiply(b, 0x0d) ^ Multiply(c, 0x09) ^ Multiply(d, 0x0e);
}


void masking_Init(void)
{

	 
     for( int i = 0; i < 6;i++ )
     {
		#ifndef MT  
			mask_sub1 = rand()%256; //mask1
			mask_sub2 = rand()%256; //mask2
			mask1 = rand()%256;   //mask3
			mask2 = rand()%256;   //mask4
			mask3 = rand()%256;   //mask5
			mask4 = rand()%256;   //mask6        
        #endif
        
        #ifdef MT
			mask_sub1 = XORSHIFTout(); //mask1
			mask_sub2 = XORSHIFTout(); //mask2
			mask1 = XORSHIFTout();     //mask3
			mask2 = XORSHIFTout();     //mask4
			mask3 = XORSHIFTout();     //mask5
			mask4 = XORSHIFTout();     //mask6
        #endif
        
     }
     InvMixColumns_mask(mask1,mask2,mask3,mask4);
     calcSBOX_m();
}
