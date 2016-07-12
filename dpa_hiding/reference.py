import time
import signal
import sys
import os
import random
import thread

from numpy import *

import h5py
import csv

from array import array
import numpy as np

import load_traces_hiding_preprocessing as load_traces     # Loads traces


	
def hdf5_file_init(o_file, n_traces, n_samples, chunksize_plaintext, chunksize_ciphertext, chunksize_traces):
	if os.path.isfile(o_file):
		print ("WARNING: File " + o_file + " already exists, overwriting...")		
		os.remove(o_file)
	filehandle = h5py.File(o_file)
	
	FHplaintext = filehandle.create_dataset("plaintext", (n_traces, 16), chunks=chunksize_plaintext, dtype = uint8)
	FHciphertext = filehandle.create_dataset("ciphertext", (n_traces, 16), chunks=chunksize_ciphertext, dtype = uint8)
	FHtraces = filehandle.create_dataset("traces", (n_traces, n_samples), chunks=chunksize_traces, dtype = uint8)
	
	return(filehandle, FHplaintext, FHciphertext, FHtraces)
	
def hdf5_file_close(filehandle):
	filehandle.close()
	
	
def hdf5_add_data(plaintext, ciphertext, trace, trace_number, FHplaintext, FHciphertext, FHtraces):
	 
	
	FHplaintext[trace_number, :] = plaintext;
	FHciphertext[trace_number, :] = ciphertext;
	FHtraces[trace_number, :] = trace;

def main():
	####################################################################
	# configuration start
	#open input file (path defined in load_traces)
	input_data = load_traces.load_traces_hiding_preprocessing()

	# Load measured traces into a matrix: trace-number x trace-length
	tracesOld = input_data.get_traces()
	# Load ciphertexts into a matrix: trace-number x 16 bytes ciphertext
	ciphertexts = input_data.get_ciphertexts()
	# Load plaintexts into a matrix: trace-number x 16 bytes plaintext
	plaintexts = input_data.get_plaintexts()

	n_traces    = 500
	w_traces	= n_traces
	n_samples   = 15000    # number of samples per trace
	o_directory = './'	# output directory
	o_file_name = 'reference.h5'       # output file name
	
	chunksize_plaintext = (n_traces, 16)    # defines the chunksize of the plaintext dataset in the hdf5 file
	chunksize_ciphertext = (n_traces, 16)    # defines the chunksize of the ciphertext dataset in the hdf5 file
	chunksize_traces = (n_traces, n_samples)    # defines the chunksize of the traces dataset in the hdf5 file
	
	# configuration end
	####################################################################
	# original = 70000
	# interval = 9000
	# pattern = tracesOld[0,original:original+n_samples]
	traces = [None] * n_traces
	# traces[0] = pattern
	for j in range(n_traces):
		indice = np.argmin(tracesOld[j][:], axis=0)
		# print indice
		# for index in range(indice+5000, 120000):
		# 	if tracesOld[j, index] < 100:
		# 		break;
		traces[j] = tracesOld[j, 1000:16000]

		# if len(tracesOld[j, indice-n_samples:indice]) > 1000:
		# 	traces[j] = tracesOld[j, indice-n_samples:indice]
		# else:
		# 	traces[j] = traces[j-1]

		# if len(tracesOld[j, indice-n_samples:indice]) > 1000:
		# 	traces[j] = tracesOld[j, indice-5000:indice+10000]
		# else:
		# 	traces[j] = traces[j-1]

		# errOld = 100000000000
		# # final = pattern
		# # for i in range(len(tracesOld[0])-10000)
		# indice = np.argmin(tracesOld[j][:], axis=0)
		# # if len(tracesOld[0,indice:])-500 > 0:
	 #  	for i in range(len(tracesOld[0,indice:])-n_samples):
		# 	search = tracesOld[j,i+indice:i+indice+n_samples]
		# 	if len(search) == n_samples:
		# 		err = np.sum((pattern - search)**2)
		# 		if err < errOld:
		# 			errOld = err
		# 			if err < 900000:
		# 				traces[j] = search
		# 			else:
		# 				traces[j] = pattern
		# 			if err < 600000:
		# 				print "search %d err is %d" % (j, err)
		# 				break
		# 			print "search %d err is %d" % (j, err)
		# print "%d search is finished" % j
	# p = 110000
	# find itermediate value shiftrows, before subbytes
	# for i in range(n_traces):
	# 	indice = np.argmin(tracesOld[i][:], axis=0)
	# 	# print indice
	# 	Trace = []
	# 	# Trace = tracesOld[i][p:p+10000]
	# 	Trace = tracesOld[i][:indice-5000]
	# 	# indice_mix = np.argmin(Trace[:], axis=0)
	# 	# Trace = Trace[indice_mix-500:indice_mix+500]
	# 	# Trace = [Trace[x] for x in range(len(Trace)-100) if np.mean(Trace[x:x+100]) < 135]
	# 	Trace = [Trace[x] for x in range(len(Trace)-100) if np.mean(Trace[x:x+100]) < 135]
	# 	# Trace = [tracesOld[i][x] for x in range(len(tracesOld[0])-100) if np.mean(tracesOld[i][x:x+100]) < 125]
	# 	if len(Trace) >= 10000:
	# 		traces[j] = Trace[-10000:]
	# 		print "%d is finished" % j
	# 		j = j + 1
	# 	else:
	# 		w_traces = w_traces - 1
	# print len(traces[0])
	o_file = o_directory + o_file_name
	filehandle, FHplaintext, FHciphertext, FHtraces = hdf5_file_init(o_file, n_traces, n_samples, chunksize_plaintext, chunksize_ciphertext, chunksize_traces)
	# start collecting power traces
	for i in range(w_traces):
		hdf5_add_data(plaintexts[i][:], ciphertexts[i][:], traces[i][:], i, FHplaintext, FHciphertext, FHtraces)
	# close and exit
	hdf5_file_close(filehandle)
	sys.exit(0)

if __name__ == "__main__":
	main()