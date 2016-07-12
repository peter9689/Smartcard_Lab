#include <stdint.h>
#include <stdlib.h>
#include <avr/io.h>
#include "util.h"
#include "adc.h"

//#define F_CPU 7372800UL //Programmer helper

#define F_CPU 4800000UL //Card Reader

uint32_t seed;

void ADC_Init(void)
{
  //ADMUX = (1<<REFS0);
  ADMUX = 0b01001111;   
  ADCSRA = (1<<ADPS1) | (1<<ADPS0);     // Frequency
  ADCSRA |= (1<<ADEN);                 // activate ADC   
 
  ADCSRA |= (1<<ADSC);                  // one ADC conversion
  while (ADCSRA & (1<<ADSC) ) {         // wait for result
  }

  (void) ADCW;
}


uint16_t ADC_Read(void)
{
  ADCSRA |= (1<<ADSC);            // single conversion
  while (ADCSRA & (1<<ADSC) ) {   // wait for result
  }
  return ADCW;                   
}

uint16_t getLSB(uint16_t adcval){
	return adcval & 1;
}


uint32_t createSeed32(void){
	uint8_t seedCount=0;
	uint32_t seed[1]={0};
	
	while(seedCount<32){
		uint16_t adcval1 = ADC_Read();
		uint16_t adcval2 = ADC_Read();
		
		if((getLSB(adcval1) && !getLSB(adcval2))){
			SetBit(seed,seedCount);
			seedCount++;
		}
		if((!getLSB(adcval1) && getLSB(adcval2))){
			ClearBit(seed,seedCount);
			seedCount++;
		}			
	}		
	return seed[0];
}
