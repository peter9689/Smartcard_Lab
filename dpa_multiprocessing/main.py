################################################################################
#                Skeleton script                        #
################################################################################
#                                                                              #
# Sichere Implementierung kryptographischer Verfahren WS 2015-2016             #
#                                                                              #
# Technische Universitaet Muenchen                                             #
# Institute for Security in Information Technology                             #
# Prof. Dr.-Ing. Georg Sigl                                                    #
#                                                                              #
################################################################################

############################## IMPORT MODULES ##################################

import dpa         		#  DPA implementation
import test_key         # Tests derived key
import load_traces      # Loads traces
import time
import csv              # Add support for comma separated value (CSV) files
import matplotlib.pyplot as plt
import multiprocessing 
import subprocess
from functools import partial
import numpy as np 

##import numpy as np      # Add support for matrix manipulations
########################### LOAD DATA AND TRACES ###############################

#open input file (path defined in load_traces)
input_data = load_traces.load_traces()

# Load measured traces into a matrix: trace-number x trace-length
traces = input_data.get_traces()
# Load ciphertexts into a matrix: trace-number x 16 bytes ciphertext
ciphertexts = input_data.get_ciphertexts()
# Load plaintexts into a matrix: trace-number x 16 bytes plaintext
plaintexts = input_data.get_plaintexts()

############################### PERFORM DPA ####################################

# last_round_key = dpa.perform_dpa(ciphertexts, traces)
#last_round_key = dpa.perform_dpa(ciphertexts, traces)


timeList = []
compressRate = []
rate = 40
BYTE16=16
# while(1):
if __name__ == '__main__':
	t1 = time.clock()
	last_round_key, COR , DiffTrace , TRACES, SAMPLE, dpa_init_done = dpa.perform_dpa(traces, rate)
	if dpa_init_done == True :
	    pool = multiprocessing.Pool(processes=4)
    	iterable= range(16)
    	plain=plaintexts
    	func= partial(dpa.getKeyForByte,plain,last_round_key,DiffTrace,TRACES,SAMPLE)
    	results =[ ]
    	r = pool.map(func, iterable) # Wait on the result    	 
    	pool.close();
    	pool.terminate();
    	last_round_key=np.array(r,np.uint8)
	t2 = time.clock()
	print (t2-t1)
	############################# TEST RESULTS ###################################

	if test_key.test_key(last_round_key, plaintexts[0], ciphertexts[0]):
	    print "Congratulations! Your key is right."
		    # compressRate.append(rate)
		    # rate += 50
		    # print t2 -t1
		    # timeList.append(t2 - t1)
		    # print COR
		    # plt.plot(COR, label = "rate " + str(rate))
		    # plt.ylabel('COR')
		    # plt.xlabel('KEY')
		    # plt.show()
	else:
	    print "Your key is wrong :-("
	    # plt.plot(compressRate,timeList)
	    # plt.ylabel('time')
	    # plt.xlabel('compression rate')
	    # plt.legend(loc='upper right')
	    # plt.show()
	    # break 
	############################# OUTPUT RESULTS ###################################

	last_round_key_hex = ["%02X" % last_round_key[i] for i in range(len(last_round_key)) ]
	keyF = open( "./key.txt", "w" )
	writer = csv.writer(keyF)
	writer.writerow(last_round_key_hex)
	keyF.close()
