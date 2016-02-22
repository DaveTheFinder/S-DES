import os.path

__author__ = 'Armando Minjares & David Saenz'

P4_Cons = (2, 4, 3, 1)
P10_Cons = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8_Cons = (6, 3, 7, 4, 8, 5, 10, 9)
IP_Cons = (2, 6, 3, 1, 4, 8, 5, 7)
IP_Inverse_Cons = (4, 1, 3, 5, 7, 2, 8, 6)
E_Over_P = (4, 1, 2, 3, 2, 3, 4, 1)

S0 = ((1, 0, 3, 2),
      (3, 2, 1, 0),
      (0, 2, 1, 3),
      (3, 1, 3, 2))

S1 = ((0, 1, 2, 3),
      (2, 0, 1, 3),
      (3, 0, 1, 0),
      (2, 1, 0, 3))

plain_Text,key_Text,cipher_Text,IP,P10,left_1,left_2,k1,k2,R,EP,EP_XOR_K1,L,EP_XOR_K2,fk1,fk2 = '','','','','','','','','','','','','','','',''

def type_of_job():
    if os.path.exists('Pares.txt'):
        brute_force()
    else:
        type_of_job = raw_input("What kind of job are you going to perform? \n1) Encryption \n2) Decryption \nOperation: ")
        if type_of_job == '1':
            global plain_Text 
            plain_Text = raw_input("Introduce the Plain Text to Encrypt (8 bit): ")
            #plain_Text = '00101000'
            global key_Text 
            key_Text = raw_input("Introduce the Key for the Encryption (10 bit): ")
            #key_Text = '1100011110'
            encrypt()
        elif type_of_job == '2':
            global cipher_Text 
            cipher_Text = raw_input("Introduce the Cipher Text to Decrypt (8 bit): ")
            #cipher_Text = '10001010'
            global key_Text 
            key_Text = raw_input("Introduce the Key for the Decryption (10 bit): ")
            #key_Text = '1100011110'
            decrypt()

def permutation(original, perm_key):
    output = ''
    for x in perm_key:
        output += original[x-1]
    return output

def left_shift(key_to_shift):
    left_output = ''
    right_output = ''
    left = ''
    right = ''

    first_half = key_to_shift[:len(key_to_shift)/2]
    second_half = key_to_shift[len(key_to_shift)/2:]
    first_char_left = first_half[0]
    first_char_right = second_half[0]
    left = first_half + first_char_left
    right = second_half + first_char_right

    for x in range(1,6):
        left_output += left[x]
        right_output += right[x]
    return left_output + '' + right_output 

def xor(to_xor, perm_key):
    output = ''
    for a,b in zip(to_xor,perm_key):
        output += str((int(a) + int(b)) % 2)
    return output

#To get "L". e_p_r_x this is E/P(R) xor K1
def left_param(e_p_r_x, sBox0, sBox1, side):
    left_half = ''
    right_half = ''
    row_S0 = 0
    col_S0 = 0
    row_S1 = 0
    col_S1 = 0
    left_leftSidePar, left_rightSidePar, output, output_P4, left = '', '', '', '',''

    left_half = e_p_r_x[:len(e_p_r_x)/2]
    right_half = e_p_r_x[len(e_p_r_x)/2:]

    row_S0 = int((left_half[0] + left_half[3]), 2)
    col_S0 = int((left_half[1] + left_half[2]), 2)
    row_S1 = int((right_half[0] + right_half[3]), 2)
    col_S1 = int((right_half[1] + right_half[2]), 2)
 
    left_leftSidePar = '{:02b}'.format(sBox0[row_S0][col_S0])
    left_rightSidePar = '{:02b}'.format(sBox1[row_S1][col_S1])
    
    output = left_leftSidePar + '' +left_rightSidePar
    output_P4 = permutation(output, P4_Cons)
    left = xor(output_P4, side)
    return left

def swap(left_parm, right_parm):
    new_left, new_right = '',''
    new_left = right_parm
    new_right = left_parm
    return new_left,new_right

def encrypt():
    global IP 
    IP = permutation(plain_Text, IP_Cons)
    print "IP(P) = %s" % IP
    global P10
    P10 = permutation(key_Text, P10_Cons)
    print "P10(K) = %s" % P10
    global left_1 
    left_1 = left_shift(P10)
    print "Left Shift: %s" % left_1
    global k1
    k1 = permutation(left_1, P8_Cons)
    print "K1 = %s" % k1
    global left_2
    left_2 = left_shift(left_shift(left_1))
    print "Left Shift-2: %s" % left_2
    global k2
    k2 = permutation(left_2, P8_Cons)
    print "K2 = %s" % k2
    global R
    R = IP[len(IP)/2:]
    print "R: %s" % R
    global EP
    EP = permutation(R, E_Over_P)
    print "Fk1 E/P(R): %s" % EP
    global EP_XOR_K1
    EP_XOR_K1 = xor(EP, k1)
    print "E/P(R) XOR with K1: %s" % EP_XOR_K1
    global L
    L = left_param(EP_XOR_K1, S0, S1, IP[len(IP)/2:])
    print"L (Left): %s" % L
    L,R = swap(L,R)
    print "SWAP: L = %s" % L + ", R = %s" % R
    EP = permutation(R, E_Over_P)
    print "Fk2 E/R(R): %s" % EP
    global EP_XOR_K2
    EP_XOR_K2 = xor(EP, k2)
    print "E/P(R) XOR with K2: %s" % EP_XOR_K2
    L = left_param(EP_XOR_K2, S0, S1, L)
    print"L (Left): %s" % L
    global fk2
    fk2 = L + '' + R
    print "Fk2: %s" % fk2
    global cipher_Text
    cipher_Text = permutation(fk2, IP_Inverse_Cons)
    print "(!!!) CipherText: %s" % cipher_Text

def decrypt():
    global IP 
    IP = permutation(cipher_Text, IP_Cons)
    print "IP(P) = %s" % IP
    global P10
    P10 = permutation(key_Text, P10_Cons)
    print "P10(K) = %s" % P10
    global left_1 
    left_1 = left_shift(P10)
    print "Left Shift: %s" % left_1
    global k1
    k1 = permutation(left_1, P8_Cons)
    print "K1 = %s" % k1
    global left_2
    left_2 = left_shift(left_shift(left_1))
    print "Left Shift-2: %s" % left_2
    global k2
    k2 = permutation(left_2, P8_Cons)
    print "K2 = %s" % k2
    global R
    R = IP[len(IP)/2:]
    print "R: %s" % R
    global EP
    EP = permutation(R, E_Over_P)
    print "Fk1 E/P(R): %s" % EP
    global EP_XOR_K1
    EP_XOR_K1 = xor(EP, k2)
    print "E/P(R) XOR with K2: %s" % EP_XOR_K1
    global L
    L = left_param(EP_XOR_K1, S0, S1, IP[:len(IP)/2])
    print"L (Left): %s" % L
    L,R = swap(L,R)
    print "SWAP: L = %s" % L + ", R = %s" % R
    EP = permutation(R, E_Over_P)
    print "Fk2 E/R(R): %s" % EP
    global EP_XOR_K2
    EP_XOR_K2 = xor(EP, k1)
    print "E/P(R) XOR with K1: %s" % EP_XOR_K2
    L = left_param(EP_XOR_K2, S0, S1, L)
    print"L (Left): %s" % L
    global fk2
    fk2 = L + '' + R
    print "Fk2: %s" % fk2
    global plain_Text
    plain_Text = permutation(fk2, IP_Inverse_Cons)
    print "(!!!) PlainText: %s" % plain_Text

def simple_encrypt():
    global IP 
    IP = permutation(plain_Text, IP_Cons)
    global P10
    P10 = permutation(key_Text, P10_Cons)
    global left_1 
    left_1 = left_shift(P10)
    global k1
    k1 = permutation(left_1, P8_Cons)
    global left_2
    left_2 = left_shift(left_shift(left_1))
    global k2
    k2 = permutation(left_2, P8_Cons)
    global R
    R = IP[len(IP)/2:]
    global EP
    EP = permutation(R, E_Over_P)
    global EP_XOR_K1
    EP_XOR_K1 = xor(EP, k1)
    global L
    L = left_param(EP_XOR_K1, S0, S1, R)
    L,R = swap(L,R)
    EP = permutation(R, E_Over_P)
    global EP_XOR_K2
    EP_XOR_K2 = xor(EP, k2)
    L = left_param(EP_XOR_K2, S0, S1, L)
    global fk2
    fk2 = L + '' + R
    global cipher_Text
    cipher_Text = permutation(fk2, IP_Inverse_Cons)

def simple_decrypt():
    global IP 
    IP = permutation(cipher_Text, IP_Cons)
    global P10
    P10 = permutation(key_Text, P10_Cons)
    global left_1 
    left_1 = left_shift(P10)
    global k1
    k1 = permutation(left_1, P8_Cons)
    global left_2
    left_2 = left_shift(left_shift(left_1))
    global k2
    k2 = permutation(left_2, P8_Cons)
    global R
    R = IP[len(IP)/2:]
    global EP
    EP = permutation(R, E_Over_P)
    global EP_XOR_K1
    EP_XOR_K1 = xor(EP, k2)
    global L
    L = left_param(EP_XOR_K1, S0, S1, IP[:len(IP)/2])
    L,R = swap(L,R)
    EP = permutation(R, E_Over_P)
    global EP_XOR_K2
    EP_XOR_K2 = xor(EP, k1)
    L = left_param(EP_XOR_K2, S0, S1, L)
    global fk2
    fk2 = L + '' + R
    global plain_Text
    plain_Text = permutation(fk2, IP_Inverse_Cons)

def brute_force():
    pairs = []
    with open ('Pares.txt', 'r') as the_file:
        for lines in the_file:
            for bits in lines.strip().split(','):
                pairs.append(bits)

    keys = []
    with open ('posible_keys.txt', 'r') as keys_file:
        for more_lines in keys_file:
            for keys_num in more_lines.strip().split():
                keys.append(keys_num)

    counter = 0
    length = len(pairs)/2
    possible_keys = []
    for x in range(0, 1024):
        global key_Text
        key_Text = keys[x]
        for y in range(0, length):
            if y%2 == 0:
                global cipher_Text
                cipher_Text = pairs[y+1]
                simple_decrypt()
            if plain_Text == pairs[y]:
                possible_keys.append(key_Text)
    winner_key = most_common_key(possible_keys)
    print "Key = %s" % winner_key

def most_common_key(the_list):
    return max(set(the_list), key=the_list.count)
            
type_of_job()