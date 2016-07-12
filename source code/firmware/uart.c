#include <avr/io.h> 
#include "uart.h"

//#define F_CPU 7372800UL //Programmer helper
#define F_CPU 4800000UL //Card Reader
#define BAUD 9600UL

#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)  


void USART_Init()
{
	/* Set baud rate */
	UBRR0H = (unsigned char)(UBRR_VAL>>8);
	UBRR0L = (unsigned char)UBRR_VAL;
	/* Enable receiver and transmitter */
	UCSR0B = (1<<TXEN0);
        UCSR0C = 3<<UCSZ00; //8N1
}

void USART_Transmit(unsigned char data)
{
	while(!(UCSR0A & (1<<UDRE0))){}
	UDR0 = data;
}

void uart_puts (char *s)
{
    while (*s)
    {   /* so lange *s != '\0' also ungleich dem "String-Endezeichen(Terminator)" */
        USART_Transmit(*s);
        s++;
    }
}
