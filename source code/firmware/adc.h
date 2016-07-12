#ifndef ADC_H
#define ADC_H

#ifdef TRNG
	extern uint32_t seed;
#endif

void ADC_Init(void);
uint16_t ADC_Read();

#endif
