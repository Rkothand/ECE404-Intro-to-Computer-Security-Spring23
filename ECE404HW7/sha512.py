# Homework Number: 5
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:3/6/22

import sys
import BitVector
if BitVector.__version__ < '3.2':
    sys.exit("You need BitVector module of version 3.2 or higher" )
from BitVector import *

def sha512(input, outfile):

    #  The 8 32-words used for initializing the 512-bit hash buffer before we start scanning the
    #  input message block for its hashing. See page 13 (page 17 of the PDF) of the NIST standard.
    #  Note that the hash buffer consists of 8 32-bit words named h0, h1, h2, h3, h4, h5, h6, and h7.
    h0 = BitVector(hexstring='6a09e667f3bcc908')
    h1 = BitVector(hexstring="bb67ae8584caa73b")
    h2 = BitVector(hexstring="3c6ef372fe94f82b")
    h3 = BitVector(hexstring="a54ff53a5f1d36f1")
    h4 = BitVector(hexstring="510e527fade682d1")
    h5 = BitVector(hexstring="9b05688c2b3e6c1f")
    h6 = BitVector(hexstring="1f83d9abfb41bd6b")
    h7 = BitVector(hexstring="5be0cd19137e2179")
    
    #  The K constants (also referred to as the "round constants") are used in round-based processing 
    #  of each 512-bit input message block.  There is a 32-bit constant for each of the 64 rounds. 
    #  These are as provided on page 10 (page 14 of the PDF) of the NIST standard.  Note that these 
    #  are ONLY USED in STEP 3 of the hashing algorithm where we take each 512-bit input message block 
    #  through 64 rounds of processing.
    K = ["428a2f98d728ae22", "7137449123ef65cd","b5c0fbcfec4d3b2f","e9b5dba58189dbbc","3956c25bf348b538","59f111f1b605d019","923f82a4af194f9b",
         "ab1c5ed5da6d8118","d807aa98a3030242","12835b0145706fbe","243185be4ee4b28c","550c7dc3d5ffb4e2","72be5d74f27b896f","80deb1fe3b1696b1",
         "9bdc06a725c71235","c19bf174cf692694","e49b69c19ef14ad2","efbe4786384f25e3","0fc19dc68b8cd5b5","240ca1cc77ac9c65","2de92c6f592b0275",
         "4a7484aa6ea6e483","5cb0a9dcbd41fbd4","76f988da831153b5","983e5152ee66dfab","a831c66d2db43210","b00327c898fb213f","bf597fc7beef0ee4",
         "c6e00bf33da88fc2","d5a79147930aa725","06ca6351e003826f","142929670a0e6e70","27b70a8546d22ffc","2e1b21385c26c926","4d2c6dfc5ac42aed",
         "53380d139d95b3df","650a73548baf63de","766a0abb3c77b2a8","81c2c92e47edaee6","92722c851482353b","a2bfe8a14cf10364","a81a664bbc423001",
         "c24b8b70d0f89791","c76c51a30654be30","d192e819d6ef5218","d69906245565a910","f40e35855771202a","106aa07032bbd1b8","19a4c116b8d2d0c8",
         "1e376c085141ab53","2748774cdf8eeb99","34b0bcb5e19b48a8","391c0cb3c5c95a63","4ed8aa4ae3418acb","5b9cca4f7763e373","682e6ff3d6b2b8a3",
         "748f82ee5defb2fc","78a5636f43172f60","84c87814a1f0ab72","8cc702081a6439ec","90befffa23631e28","a4506cebde82bde9","bef9a3f7b2c67915",
         "c67178f2e372532b","ca273eceea26619c","d186b8c721c0c207","eada7dd6cde0eb1e","f57d4f7fee6ed178","06f067aa72176fba","0a637dc5a2c898a6",
         "113f9804bef90dae","1b710b35131c471b","28db77f523047d84","32caab7b40c72493","3c9ebe0a15c9bebc","431d67c49c100d4c","4cc5d4becb3e42b6",
         "597f299cfc657e2a","5fcb6fab3ad6faec","6c44198c4a475817"]
    
    #  Store the 64 K constants as an array of BitVector objects:
    K_bv = [BitVector(hexstring = k_constant) for k_constant in K]

    #  STEP 1 OF THE HASHING ALGORITHM: Pad the input message so that its length is an integer multiple
    #                                   of the block size which is 512 bits.  This padding must account
    #                                   for the fact that the last 64 bit of the padded input must store
    #                                   length of the input message:
    length = input.length()
    bv1 = input + BitVector(bitstring="1")
    length1 = bv1.length()
    howmanyzeros = (896 - length1) % 1024
    zerolist = [0] * howmanyzeros
    bv2 = bv1 + BitVector(bitlist = zerolist)
    bv3 = BitVector(intVal = length, size = 128)
    bv4 = bv2 + bv3
    
    #  Initialize the array of "words" for storing the message schedule for a block of the input message:
    words = [None] * 80
    
    for n in range(0,bv4.length(),1024):
        block = bv4[n:n+1024]
    
        #  STEP 2 OF THE HASHING ALGORITHM: Now we need to create a message schedule for this 512-bit 
        #                                   input block.  The message schedule contains 64 words, each 
        #                                   32-bits long.  
        #                                   As shown below, the first 16 words of the message schedule 
        #                                   are obtained directly from the 512-bit input block:
        words[0:16] = [block[i:i+64] for i in range(0,1024,64)]
        #  Now we need to expand the first 16 32-bit words of the message schedule into a full schedule 
        #  that contains 64 32-bit words. This involves using the functions sigma0 and sigma1 as shown 
        #  below:
        for i in range(16, 80):                      
            i_minus_2_word = words[i-2]
            i_minus_15_word = words[i-15]
            #  The sigma1 function is applied to the i_minus_2_word and the sigma0 function is applied to 
            #  the i_minus_15_word:
            sigma0 = (i_minus_15_word.deep_copy() >> 1) ^ (i_minus_15_word.deep_copy() >> 8) ^ \
                                                            (i_minus_15_word.deep_copy().shift_right(7))
            sigma1 = (i_minus_2_word.deep_copy() >> 19) ^ (i_minus_2_word.deep_copy() >> 61) ^ \
                                                            (i_minus_2_word.deep_copy().shift_right(6))
            words[i] = BitVector(intVal=(int(words[i-16]) + int(sigma1) + int(words[i-7]) + \
                                                                    int(sigma0)) & 0xFFFFFFFFFFFFFFFF, size=64)
    
        #  Before we can start STEP 3, we need to store the hash buffer contents obtained from the 
        #  previous input message block in the variables a,b,c,d,e,f,g,h:
        a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7
    
        #  STEP 3 OF THE HASHING ALGORITHM: In this step, we carry out a round-based processing of a
        #                                   512-bit input message block.  There are a total of 64 
        #                                   rounds and the calculations carried out in each round are 
        #                                   referred to as calculating a "round function".  The round 
        #                                   function for the i-th round consists of permuting the
        #                                   previously calculated contents of the hash buffer 
        #                                   registers as stored in the temporary variables 
        #                                   a,b,c,d,e,f,g and replacing the values of two of these 
        #                                   variables with values that depend of the i-th word in the 
        #                                   message schedule, words[i],  and i-th round constant, K[i]. 
        #                                   As you see below, this requires that we first calculate 
        #                                   the functions ch, maj, sum_a, and sum_e.
        for i in range(80):
            ch = (e & f) ^ ((~e) & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            sum_a = ((a.deep_copy()) >> 28) ^ ((a.deep_copy()) >> 34) ^ ((a.deep_copy()) >> 39)
            sum_e = ((e.deep_copy()) >> 14) ^ ((e.deep_copy()) >> 18) ^ ((e.deep_copy()) >> 41)
            t1 = BitVector(intVal=(int(h) + int(ch) + int(sum_e) + int(words[i]) + int(K_bv[i])) & \
                                                                                    0xFFFFFFFFFFFFFFFF, size=64)
            t2 = BitVector(intVal=(int(sum_a) + int(maj)) & 0xFFFFFFFFFFFFFFFF, size=64)
            h = g
            g = f
            f = e
            e = BitVector(intVal=(int(d) + int(t1)) & 0xFFFFFFFFFFFFFFFF, size=64)
            d = c
            c = b
            b = a
            a = BitVector(intVal=(int(t1) + int(t2)) & 0xFFFFFFFFFFFFFFFF, size=64)
    
        #  STEP 4 OF THE HASHING ALGORITHM:  The values in the temporary variables a,b,c,d,e,f,g,h 
        #                                    AFTER 64 rounds of processing are now mixed with the 
        #                                    contents of the hash buffer as calculated for the 
        #                                    previous block of the input message:
        h0 = BitVector( intVal = (int(h0) + int(a)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h1 = BitVector( intVal = (int(h1) + int(b)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h2 = BitVector( intVal = (int(h2) + int(c)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h3 = BitVector( intVal = (int(h3) + int(d)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h4 = BitVector( intVal = (int(h4) + int(e)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h5 = BitVector( intVal = (int(h5) + int(f)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h6 = BitVector( intVal = (int(h6) + int(g)) & 0xFFFFFFFFFFFFFFFF, size=64 )
        h7 = BitVector( intVal = (int(h7) + int(h)) & 0xFFFFFFFFFFFFFFFF, size=64 )
    
    #  Concatenate the contents of the hash buffer to obtain a 512-element BitVector object:
    message_hash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    #  Get the hex representation of the binary hash value:
    hash_hex_string = message_hash.getHexStringFromBitVector()
    outfile.write(hash_hex_string)

def main():
    input = sys.argv[1]
    infile = open(input, 'r')
    infile = BitVector(textstring=infile.read())
    output =sys.argv[2]
    outfile = open(output, 'w')
    sha512(infile, outfile) 


main()