#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; coding: utf8 -*-
"""
DPA Attack on last round key of AES.

Please implement your attack in the function perform_dpa().
"""
############################## IMPORT MODULES ##################################
import numpy as np      # numeric calculations and array
import math
from scipy.stats.stats import pearsonr 
import multiprocessing 
########################## CONSTANTS DEFINITION ################################

SBox = np.array([
0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
], np.uint8)
# Byte Hamming Weight Table
hamming_weight = np.array([
0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8
], np.uint8)



COR = np.zeros(16, np.float32)
# TODO: Please implement your attack here!
BYTE16, KEY256 = 16, 256          # BYTE:number of bytes      #KEY:number of key hypotheses
#DiffTrace = traces
#############################comprese  and caculate#############
#compress the data of the trace with mean
# RATE = 500
# SAMPLE = SAMPLE/RATE   #new SAMPLE after the compression
# DiffTrace = [None] * TRACES
# for x in range(TRACES):
#     DiffTrace[x] = [0] * (SAMPLE)
# #method 1: get the sum of all compressed values
# for x in range(TRACES):
#     DiffTrace[x] = [np.mean(traces[x][y*RATE:(y+1)*RATE]) for y in range(SAMPLE)]
# print 'compression is done'

####################### IMPLEMENT YOUR ATTACK BELOW ############################

def getKeyForByte(plaintexts,last_round_key,DiffTrace,TRACES,SAMPLE,BYTE):
        KEY256=256    
        HammingWeight = [None] * TRACES #create the matrix for Hamming Weight,it contains T columns
        
        for y in range(TRACES): 
            HammingWeight[y] = ([0] * KEY256) #the row is the number of probability of key1 256

        # Plantext = [None] * TRACES #create the matrix for Hamming Weight,it contains T columns
        # for y in range(TRACES): 
        #     Plantext[y] = ([0] * KEY256) #the row is the number of probability of key1 256

        # for x in range(KEY256):
        #     for y in range(TRACES):
        #         Plantext[y][x] = np.float32(SBox[plaintexts[y][i] ^ x]) #get the hamming weight of each probabity of key
        # print Plantext[1]
        #fulfill the matrix of hamming weight
        for x in range(KEY256):
            for y in range(TRACES):
                HammingWeight[y][x] = np.float32(hamming_weight[SBox[plaintexts[y][BYTE] ^ x]]) #get the hamming weight of each probabity of key
                #HammingWeight[y][x]= np.float32(hamming_weight[(Sbox[plaintexts[y][BYTE] ^ x]) ^ (plaintexts[y][BYTE] ^ x)]) // For masking 
        # print HammingWeight
        #calculate the mean of hammingweight in each row(each key)          
        MeanHM = np.zeros(KEY256, np.float32)
        MeanHM1 = np.zeros(KEY256, np.float32)
        MeanHM = np.array(map(sum,zip(*HammingWeight)))/TRACES * 1.0
        for y in range(TRACES):
            HammingWeight[y] = HammingWeight[y] - MeanHM
        HammingWeight1 = np.array(map(list, zip(*HammingWeight)))
        print 'power model', BYTE, 'is finished'
        DiffTrace1 = np.array(map(list, zip(*DiffTrace)))
        NowCOR = 0
        MaxCOR = 0
        NowKey = 0

        for x in range(KEY256):
            dem1 = np.sum((HammingWeight1[x][:])**2)
            for y in range(SAMPLE):
                d1 = np.sum(HammingWeight1[x][:]*DiffTrace1[y][:])
                dem2 = np.sum((DiffTrace1[y][:])**2)
                NowCOR = abs(d1 / (math.sqrt(dem1)*math.sqrt(dem2)) * 1.0)
                if NowCOR > MaxCOR:
                    MaxCOR = NowCOR
                    NowKey = x

        #calculate correlations 
        print 'key ', BYTE, 'is finished'
        return NowKey

def calculateCorrelations(BYTE,DiffTrace,last_round_key,HammingWeight1):
        return 0 
        
#             # print "The", i + 1, "Nowkey is", x, "Maxkey is", NowKey, "correlations is", MaxCOR
#         #     last_round_key[BYTE] = NowKey
#         #     COR[BYTE] = MaxCOR        
#         #     # print COR[i]
#         #     
#         # print "key for" ,BYTE,": ",last_round_key[BYTE]

def perform_dpa(traces, rate):
    global BYTE16
    global TRACES
    global SAMPLE
    global RATE
    ############################# PERFORM DPA ##################################
    #last_round_key = np.zeros(16, np.uint8)
    #COR = np.zeros(16, np.float32)
    # TODO: Please implement your attack here!
    TRACES, SAMPLE = traces.shape     # TRACES:number of traces     #SAMPLES:number of samples
    #BYTE16, KEY256 = 16, 256          # BYTE:number of bytes      #KEY:number of key hypotheses
    #DiffTrace = traces
    #############################comprese  and caculate#############
    #compress the data of the trace with mean
    # RATE = 500
    # SAMPLE = SAMPLE/RATE   #new SAMPLE after the compression
    # DiffTrace = [None] * TRACES
    # for x in range(TRACES):
    #     DiffTrace[x] = [0] * (SAMPLE)
    # #method 1: get the sum of all compressed values
    # for x in range(TRACES):
    #     DiffTrace[x] = [np.mean(traces[x][y*RATE:(y+1)*RATE]) for y in range(SAMPLE)]
    # print 'compression is done'

    RATE = rate
    SAMPLE = SAMPLE/RATE   #new SAMPLE after the compression
    DiffTrace = [None] * TRACES
    for x in range(TRACES):
        DiffTrace[x] = [0] * (SAMPLE)
    #method 1: get the sum of all compressed values
    for x in range(TRACES):
        DiffTrace[x] = [np.sum(abs(traces[x][y*RATE:(y+1)*RATE])) for y in range(SAMPLE)]
    print 'compression is done'

    #choose the biggest value
    # RATE = rate
    # SAMPLE = SAMPLE/RATE   #new SAMPLE after the compression
    # DiffTrace = [None] * TRACES
    # for x in range(TRACES):
    #     DiffTrace[x] = [0] * (SAMPLE)
    # #method 1: get the sum of all compressed values
    # for x in range(TRACES):
    #     DiffTrace[x] = [np.max(traces[x][y*RATE:(y+1)*RATE]) for y in range(SAMPLE)]
    # print 'compression is done'
    # get Mean of the traces
    MeanSample = np.array(map(sum,zip(*DiffTrace)))* 1.0/TRACES * 1.0

    DiffTrace1 = np.array(DiffTrace)
    for y in range(TRACES):
        DiffTrace[y] = DiffTrace[y] - MeanSample
    print 'traces mean is done'
	######################### Preprocessing for Masking Attack #######################
	#preprocessing is done using absolute difference
	DiffTraceMasking = np.array(DiffTrace)
	rowsTrace,columnsTrace=DiffTraceMasking.shape
	print DiffTraceMasking.shape
	preprocessed=np.zeros((rowsTrace,((columnsTrace -1)*columnsTrace )/2)) 
	begin=1
	end=0
	for i in range (1,columnsTrace):
		end= begin + columnsTrace-i-1
		preprocessed[:,begin:end]=abs(DiffTraceMasking[:,i+1:columnsTrace] - DiffTraceMasking[:,i:i+1])
		begin=end + 1;	
	##################################################################################
    last_round_key = np.zeros(16, np.uint8)
    ######################### Done, OUTPUT RESULTS ############################

    return last_round_key, COR , DiffTrace , TRACES, SAMPLE ,True
