import time
import signal
import sys
import os
import random
import thread
import matplotlib.pyplot as plt # Add support for drawing figures
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
	input_data  = load_traces.load_traces_hiding_preprocessing()
	# Load measured traces into a matrix: trace-number x trace-length
	tracesOld   = input_data.get_traces()
	ref_data    = input_data.get_ref_traces()
	# Load ciphertexts into a matrix: trace-number x 16 bytes ciphertext
	ciphertexts = input_data.get_ciphertexts()
	# Load plaintexts into a matrix: trace-number x 16 bytes plaintext
	plaintexts  = input_data.get_plaintexts()

	n_traces    = 800
	w_traces    = n_traces
	n_samples   = 10700 # number of samples per trace
	n_samples1  = 1700
	n_samples2  = 9000
	o_directory = './'	# output directory
	o_file_name = 'hiding_preprocessing_part_all.h5'       # output file name
	
	chunksize_plaintext  = (n_traces, 16)    # defines the chunksize of the plaintext dataset in the hdf5 file
	chunksize_ciphertext = (n_traces, 16)    # defines the chunksize of the ciphertext dataset in the hdf5 file
	chunksize_traces     = (n_traces, n_samples)    # defines the chunksize of the traces dataset in the hdf5 file
	
	# configuration end
	####################################################################
	traces   = [None] * n_traces
	traces1  = [None] * n_traces
	traces2  = [None] * n_traces
	
	pattern1 = tracesOld[10,48100:49800]
	pattern2 = tracesOld[10,66500:75500]

	# plt.plot(tracesOld[10,:])
	# plt.show()
	# search the first pattern
	for j in range(n_traces):
		# find the lowest value in the trace
		indice = np.argmin(tracesOld[j][:], axis=0)
		# original error
		errOld = 100000000000
		for i in range(indice-5000,indice+3000):
			search = tracesOld[j,i:i+n_samples1]
			if len(search) == n_samples1:
				err = np.sum((pattern1 - search)**2)
				if err < errOld:
					errOld     = err
					traces1[j] = search
		print "pattern1 search %d MSE is %d" % (j, 1.0*err/n_samples)
	# search the second pattern
	for j in range(n_traces):
		# find the lowest value in the trace
		indice = np.argmin(tracesOld[j][:], axis=0)
		errOld = 100000000000
		for i in range(indice,len(tracesOld[0,:])-n_samples2-10000):
			search = tracesOld[j,i:i+n_samples2]
			if len(search) == n_samples2:
				err = np.sum((pattern2 - search)**2)
				if err < errOld:
					errOld     = err
					traces2[j] = search
		print "pattern2 search %d MSE is %d" % (j, 1.0*err/n_samples)
		# combine the two patterns together
		traces[j] = np.concatenate((traces1[j],traces2[j]),axis=0)
	# write to the h5 file and save
	o_file = o_directory + o_file_name
	filehandle, FHplaintext, FHciphertext, FHtraces = hdf5_file_init(o_file, n_traces, n_samples, chunksize_plaintext, chunksize_ciphertext, chunksize_traces)
	# start collecting power traces
	for i in range(w_traces):
		hdf5_add_data(plaintexts[i][:], ciphertexts[i][:], traces[i][:], i, FHplaintext, FHciphertext, FHtraces)
	# close and exit
	hdf5_file_close(filehandle)
	# plt.plot(pattern)
	# plt.show()
	sys.exit(0)

if __name__ == "__main__":
	main()