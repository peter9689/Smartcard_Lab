#ifndef MASKING_H
#define MASKING_H



extern uint8_t mask_sub1, mask_sub2;
// the 4 masks for the mix-column
extern uint8_t mask1, mask2, mask3, mask4;
// the 4 masks after the mix-column
extern uint8_t mask11, mask22, mask33, mask44;
// the mask sbox
extern uint8_t rsbox_m[];
//the order of the sequence

void ReMask(void);
void masking_Init(void);
void InvMixColumns_mask(int a, int b, int c, int d);
void calcSBOX_m(void);
uint8_t getSBox_mInvert(uint8_t num);

#endif
