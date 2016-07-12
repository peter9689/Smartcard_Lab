#ifndef MAIN_H
#define MAIN_H


int sendBit(unsigned char bit);
int sendByte(unsigned char byte);
unsigned char receiveBit();
unsigned char receiveByte();

int init_receive();

int printBuffer();

int getData();
int compareResponse(uint8_t* response);
int copyBuff(uint8_t* ctext);


#endif
