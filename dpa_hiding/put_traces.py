# -- coding: utf-8 --
import os
import h5py           # Add support for hdf5 files
import numpy as np    # Add support for matrix manipulations

############################ DEFINE PARAMETERS #################################

# traces_path = './traces_21_06_500_31250.h5'
traces_path_put = './'
class put_traces:
    def __init__(self, traces_path = traces_path_put, plaintext, traces):
        with h5py.File('hiding_preprocessing.hdf5','w') as f:
            group = f.create_group('a_group')
            group.create_dataset(name='traces', data=traces, chunks=True, compression='gzip')
            group.create_dataset(name='plaintext', data=plaintext, chunks=True, compression='gzip')

