# __Benchmarks__ 


## __Performance:__


### Execution time

|**Implementation**|**Time [ms]**|
| ------------- |:-------------:|
| Reference card | 4.45 | 
| Own implementation (no countermeasure)|  2.7  |
| Own implementation + Dummy Operations | 14.1 (avg) |
| Own implementation + Shuffling | 7.2 |
| Own implementation + Masking | 9.6 |
| Own implementation + all countermeasures | 25 |



### Memory usage

|**Implementation**|**Program [Bytes]**|**Data [Bytes]**|
| ------------- |:-------------:| :-----:|
| Own implementation (no countermeasure)| 3846 | 2023 |
| Own implementation + Dummy Operations | 4942 | 2080 |
| Own implementation + Shuffling | 4884 | 2040 |
| Own implementation + Masking | 5372 | 2470 |
| Own implementation + Dummy + Shuffling | 4976 | 2080 |
| Own implementation + Shuffling + Masking | 6092 | 2482 |
| Own implementation + Dummy + Masking | 6144 | 2522 |
| Own implementation + all countermeasures | 6184 | 2522 |



## __Security:__ 

### DPA Attack 

|**Implementation**|**Broken [yes/no]**|**No. of Traces**|**Time [s]**|
| ------------- |:-------------:| :-----:| :-----:|
| Reference card | YES  | 170 | 70s|
| Reference card | YES  | 800 | 6.3s|
| Own implementation (no countermeasure)| YES | 800 | 5.9s |
| Own implementation (no countermeasure)| YES | 300 | 85s |
| Own implementation + Dummy Operations | YES  | 800  | 72s  |
| Own implementation + Shuffling |  |  |  |
| Own implementation + Masking | NO  | 10000 | - |
| Own implementation + Masking m=m' | YES | 800 | 11s |
| Own implementation + other countermeasure (specify)  |  |  |  |


