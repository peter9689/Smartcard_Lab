//#define F_CPU 7372800UL //Programmer helper
#define F_CPU 4800000UL //Card Reader

#include <avr/io.h>
#include <util/delay.h>
#include <util/parity.h>
#include <avr/interrupt.h>
#include <util/delay_basic.h>
#include "XORShift.h"
#include "main.h"
#include "aes.h"

#ifdef TRNG
	#include "adc.h"
#endif


#ifdef DDEBUG
	#include "uart.h"
#endif


uint8_t buffCount=0;
unsigned char inBuffer[16];
uint8_t buffer[16];

int main(void)
{
	uint8_t flag =0;
	uint8_t flag1 =0;
	uint8_t flag2 =0;
	uint8_t key[] = {0xB5,0x2E,0x33,0xB1,0x2A,0x71,0x1D,0xCB,0xF9,0xA7,0x8A,0xD7,0x39,0xD8,0x82,0x08};
	unsigned char response[5] = {0x88,0x10,0x00,0x00,0x10};
	unsigned char ctext[16];

	#ifdef DDEBUG
		USART_Init();
	#endif
	
	AesInit(key);

	//set debug bin as output PINB2:LED , PINB4: Trigger
	DDRB|=(1<<PINB2);
	DDRB|=(1<<PINB4);

	PORTB &= ~(1<<PINB2);

	DDRB|=(1<<PINB6);
	PORTB|=(1<<PINB6);
	
	#ifdef TRNG
		ADC_Init();
		seed = createSeed32();
	#endif

	_delay_ms(1);
	send_ATR();


	init_receive();

	
	while(1)
	{	
		if(buffCount>4 && !flag){
			flag=1;
			buffCount=0;
			PCMSK1 &= ~(1<<PCINT14);
			sendByte(0x10);
			DDRB &= ~(1<<PINB6); 
			PCMSK1 |= (1<<PCINT14);
		}
		if(buffCount>15 && !flag1){
			copyBuff(ctext);
			flag1=1;
			buffCount=0;
			PCMSK1 &= ~(1<<PCINT14);
			sendByte(0x61);
			sendByte(0x10);
			DDRB &= ~(1<<PINB6);
			PCMSK1 |= (1<<PCINT14);
		}
		if(buffCount>4 && !flag2){
			flag2=1;
			buffCount=0;

			PORTB |= (1<<PINB4); //Set Trigger
			AES128_ECB_decrypt(ctext, buffer);
			PORTB &= ~(1<<PINB4); //Clear Trigger

			//printBuffc();

			PCMSK1 &= ~(1<<PCINT14);
			sendByte(0xC0);
			_delay_ms(5);
			sendBuff();
			_delay_ms(10);
			sendByte(0x90);
			sendByte(0x00);

			DDRB &= ~(1<<PINB6); 
			PCMSK1 |= (1<<PCINT14);
 
			//repeat for video stream
			flag=0;
			flag1=0;
			flag2=0;
		}
		
/*
		if(buffCount>4 && !flag){
		printBuffer();

			if(compareResponse()){
				flag=1;
				buffCount=0;
				sendByte("0xEF");
				init_receive();
			}
		
		
		}
		if(buffCount>0 && flag){
		printBuffer();
		buffCount=0;
		sendByte("0xEF");
		init_receive();	
		}
*/		 
	#ifdef TRNG
		seed = createSeed32();
		#ifdef MT
			//seedRNG(seed);
			XORSHIFTseed(0);
		#else
			srand(seed);
		#endif
	#else
		#ifdef MT
			XORSHIFTseed(0);
		#else
			srand(rand());
		#endif
    #endif  
		_delay_ms(5);
	}
}

int sendBuff(){
	for(int i = 0; i < 16; i++){
		sendByte(buffer[i]);
 	}
}

#ifdef DDEBUG
int printBuffc(){
	for(int i = 0; i < 16; i++){
		USART_Transmit(buffer[i]);
 	}
	USART_Transmit(0x0A);
}
#endif

int copyBuff(uint8_t* ctext){
	for(int i=0; i<16;i++){
		ctext[i]=inBuffer[i];
	}	

}

int compareResponse(uint8_t* response){
	for(int i=0; i<5;i++){
		if(inBuffer[i]!=response[i]){
 			return 0;
		}
	}
	return 1;
}

int send_ATR(){
	sendByte(0x3B);
	sendByte(0x90);
	sendByte(0x11);
	sendByte(0x00);
}

int init_receive(){
	DDRB &= ~(1<<PINB6); //set I/O Pin as input
	PCMSK1 |= (1<<PCINT14); //pin change interrupt is enabled on the corresponding I/O pin
	PCICR |= (1<<PCIE1);  
	sei(); 
}
#ifdef DDEBUG
int printBuffer(){
	for(int i = 0; i < buffCount; i++){
		USART_Transmit(inBuffer[i]);
 	}
	USART_Transmit(0x0A);
}
#endif
int toggle(){
	PORTB |= (1<<PINB4);
	PORTB &= ~(1<<PINB4);
}


int sendByte(unsigned char byte){

	DDRB|=(1<<PINB6); //set I/O Pin as output
	sendBit(0); //start bit

	for (int i = 0; i < 8; ++i) {	
		sendBit((byte >> i) & 1);
	}

	sendBit(parity_even_bit(byte)); 
	sendBit(1); //stopBit

	return 0;
}

int sendBit(unsigned char bit){

	if(bit==1){
		PORTB|=(1<<PINB6);
	}

	else{
		PORTB&=~(1<<PINB6);
	}
	_delay_us(70);
	//_delay_loop_1(105);
	return 0;
}

unsigned char receiveByte(){
	unsigned char byte=0;
	unsigned char parity;

	for (int i = 0; i < 8; ++i) {	
		if(receiveBit()){
			byte |= (1<<i);
		}
		else{
			byte &= ~(1<<i);
		}

		_delay_loop_1(108);
	}
	
	receiveBit(); //parity
	_delay_loop_1(108);
	parity=parity_even_bit(byte);
	
	receiveBit();	
	_delay_loop_1(108);//stop bit

	return byte;
}

unsigned char receiveBit(){
	unsigned char result=0;
	//toggle();
	result = PINB & (1<<PINB6);

	return result;
}


ISR(PCINT1_vect)
{
	//test falling edge	

	_delay_loop_1(160); //wait 1.5 etu

	inBuffer[buffCount]=receiveByte();
	buffCount++;
		
	PCIFR=1<<PCIF1;  //Clear interrupt flag
}
