
# Copyright 2020
# Ahmet Can Mert <ahmetcanmert@sabanciuniv.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

DEBUG_MODE_NTT  = 0
DEBUG_MODE_INTT = 0

# Modular inverse (https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

# Bit-Reverse integer
def intReverse(a,n):
    b = ('{:0'+str(n)+'b}').format(a)
    return int(b[::-1],2)

# Bit-Reversed index
def indexReverse(a,r):
    n = len(a)
    b = [0]*n
    for i in range(n):
        rev_idx = intReverse(i,r)
        b[rev_idx] = a[i]
    return b

# forward ntt (takes input in normal order, produces output in bit-reversed order)
def IterativeForwardNTT(arrayIn, P, W, R):
    #########################################################
    if DEBUG_MODE_NTT:
        A_ntt_interm_1 = open("NTT_DIN_DEBUG_1.txt","w") # Just result
        A_ntt_interm_2 = open("NTT_DIN_DEBUG_2.txt","w") # BTF inputs
    #########################################################

    arrayOut = [0] * len(arrayIn)
    N = len(arrayIn)

    for idx in range(N):
        arrayOut[idx] = arrayIn[idx]

    #########################################################
    if DEBUG_MODE_NTT:
        A_ntt_interm_1.write("------------------------------ input: \n")
        A_ntt_interm_2.write("------------------------------ input: \n")
        for idx in range(N):
            A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
            A_ntt_interm_2.write(str(arrayOut[idx])+"\n")
    #########################################################

    v = int(math.log(N, 2))

    for i in range(0, v):
        #########################################################
        if DEBUG_MODE_NTT:
            A_ntt_interm_1.write("------------------------------ stage: "+str(i)+"\n")
            A_ntt_interm_2.write("------------------------------ stage: "+str(i)+"\n")
        #########################################################
        for j in range(0, (2 ** i)):
            for k in range(0, (2 ** (v - i - 1))):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = (W ** ((2 ** i) * k)) % P

                as_temp = arrayOut[s]
                at_temp = arrayOut[t]

                arrayOut[s] = (as_temp + at_temp) % P
                arrayOut[t] = ((as_temp - at_temp) * w) % P

                #########################################################
                if DEBUG_MODE_NTT:
                    A_ntt_interm_2.write((str(s)+" "+str(t)+" "+str(((2 ** i) * k))).ljust(16)+"("+str(as_temp).ljust(12)+" "+str(at_temp).ljust(12)+" "+str((w*R) % P).ljust(12)+") -> ("+str(arrayOut[s]).ljust(12)+" "+str(arrayOut[t]).ljust(12)+")"+"\n")
                #########################################################

        #########################################################
        if DEBUG_MODE_NTT:
            for idx in range(N):
                A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
        #########################################################

    #########################################################
    if DEBUG_MODE_NTT:
        A_ntt_interm_1.write("------------------------------ result: \n")
        A_ntt_interm_2.write("------------------------------ result: \n")
        for idx in range(N):
            A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
            A_ntt_interm_2.write(str(arrayOut[idx])+"\n")
    #########################################################

    #########################################################
    if DEBUG_MODE_NTT:
        A_ntt_interm_1.close()
        A_ntt_interm_2.close()
    #########################################################

    return arrayOut

# inverse ntt (takes input in normal order, produces output in bit-reversed order)
def IterativeInverseNTT(arrayIn, P, W, R):
    #########################################################
    if DEBUG_MODE_INTT:
        A_ntt_interm_1 = open("test/INTT_DIN_DEBUG_1.txt","w") # Just result
        A_ntt_interm_2 = open("test/INTT_DIN_DEBUG_2.txt","w") # BTF inputs
    #########################################################

    arrayOut = [0] * len(arrayIn)
    N = len(arrayIn)

    for idx in range(N):
        arrayOut[idx] = arrayIn[idx]

    #########################################################
    if DEBUG_MODE_INTT:
        A_ntt_interm_1.write("------------------------------ input: \n")
        A_ntt_interm_2.write("------------------------------ input: \n")
        for idx in range(N):
            A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
            A_ntt_interm_2.write(str(arrayOut[idx])+"\n")
    #########################################################

    v = int(math.log(N, 2))

    for i in range(0, v):
        #########################################################
        if DEBUG_MODE_INTT:
            A_ntt_interm_1.write("------------------------------ stage: "+str(i)+"\n")
            A_ntt_interm_2.write("------------------------------ stage: "+str(i)+"\n")
        #########################################################
        for j in range(0, (2 ** i)):
            for k in range(0, (2 ** (v - i - 1))):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = (W ** ((2 ** i) * k)) % P

                as_temp = arrayOut[s]
                at_temp = arrayOut[t]

                arrayOut[s] = (as_temp + at_temp) % P
                arrayOut[t] = ((as_temp - at_temp) * w) % P

                #########################################################
                if DEBUG_MODE_INTT:
                    A_ntt_interm_2.write((str(s)+" "+str(t)+" "+str(((2 ** i) * k))).ljust(16)+"("+str(as_temp).ljust(12)+" "+str(at_temp).ljust(12)+" "+str((w*R) % P).ljust(12)+") -> ("+str(arrayOut[s]).ljust(12)+" "+str(arrayOut[t]).ljust(12)+")"+"\n")
                #########################################################

        #########################################################
        if DEBUG_MODE_INTT:
            for idx in range(N):
                A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
        #########################################################

    #########################################################
    if DEBUG_MODE_INTT:
        A_ntt_interm_1.write("------------------------------ result: \n")
        A_ntt_interm_2.write("------------------------------ result: \n")
        for idx in range(N):
            A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
            A_ntt_interm_2.write(str(arrayOut[idx])+"\n")
    #########################################################

    N_inv = modinv(N, P)
    for i in range(N):
        arrayOut[i] = (arrayOut[i] * N_inv) % P

    #########################################################
    if DEBUG_MODE_INTT:
        A_ntt_interm_1.write("------------------------------ result (with N_inv): \n")
        A_ntt_interm_2.write("------------------------------ result (with N_inv): \n")
        for idx in range(N):
            A_ntt_interm_1.write(str(arrayOut[idx])+"\n")
            A_ntt_interm_2.write(str(arrayOut[idx])+"\n")
    #########################################################

    #########################################################
    if DEBUG_MODE_INTT:
        A_ntt_interm_1.close()
        A_ntt_interm_2.close()
    #########################################################

    return arrayOut
