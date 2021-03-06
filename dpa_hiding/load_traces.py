################################################################################
#                       Loading of traces from hdf5 file                       #
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
# -- coding: utf-8 --
import os
import h5py           # Add support for hdf5 files
import numpy as np    # Add support for matrix manipulations

############################ DEFINE PARAMETERS #################################

# traces_path = './traces_21_06_500_31250.h5'
# traces_path = './10rounds.h5'
# traces_path = './traces_13000.h5'
# traces_path = './traces_phase1_YL.h5'
# traces_path = './hiding_preprocessing.h5'
traces_path = './traces_13000.h5'
#traces_path = './hiding_preprocessing_part_all.h5'


########################### LOAD DATA AND TRACES ###############################

class load_traces:
    """Class used to load traces measured with measuring script."""
    def __init__(self, traces_path = traces_path):
        self.hdf5_file   = h5py.File(traces_path, "r")

    def get_traces(self):
        """Returns measured traces in a matrix: trace-number x trace-length"""
        traces = self.hdf5_file["traces"][:].astype(np.long)
        # trace = traces[:50,:]
        return traces

    def get_ciphertexts(self):
        """Returns ciphertexts in a matrix: trace-number x 16 bytes ciphertext"""
        ciphertexts  = self.hdf5_file["ciphertext"][:].astype(np.uint8)
        return ciphertexts

    def get_plaintexts(self):
        """Returns plaintexts in a matrix: trace-number x 16 bytes plaintext"""
        plaintexts  = self.hdf5_file["plaintext"][:].astype(np.uint8)
        return plaintexts

