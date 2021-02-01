# Parametric NTT/INTT Hardware

This repository provides the baseline version of Verilog code for parametric NTT/INTT hardware published in "<a href="https://ieeexplore.ieee.org/document/9171507">An Extensive Study of Flexible Design Methods for the Number Theoretic Transform</a>".

You have to set three parameters defined in `defines.v`:
* `DATA_SIZE_ARB`: bit-size of coefficient modulus *q* (constrained for values between 8-64 for practical implementations)
* `RING_SIZE`: degree of ring polynomial, namely *n* in *x^n+1* (needs to be a power of 2)
* `PE_NUMBER`: number of processing elements (*butterfly units*) (needs to be a power of 2 and `PE_NUMBER` <= `RING_SIZE`/2)

Other versions of the hardware generator and documentation will be available soon.
