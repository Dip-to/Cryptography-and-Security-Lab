from BitVector import *
import S_Box
import RoundKey

BLOCK_SIZE = 64

expansion_permutation = [31,  0,  1,  2,  3,  4, 
                          3,  4,  5,  6,  7,  8, 
                          7,  8,  9, 10, 11, 12, 
                         11, 12, 13, 14, 15, 16, 
                         15, 16, 17, 18, 19, 20, 
                         19, 20, 21, 22, 23, 24, 
                         23, 24, 25, 26, 27, 28, 
                         27, 28, 29, 30, 31, 0]

initial_permutation_matrix = [  
        57, 49, 41, 33, 25, 17,  9,  1,
        59, 51, 43, 35, 27, 19, 11,  3,
        61, 53, 45, 37, 29, 21, 13,  5,
        63, 55, 47, 39, 31, 23, 15,  7,
        56, 48, 40, 32, 24, 16,  8,  0,
        58, 50, 42, 34, 26, 18, 10,  2,
        60, 52, 44, 36, 28, 20, 12,  4,
        62, 54, 46, 38, 30, 22, 14,  6  ]

initial_reverse_permutation_matrix = [  
                39,  7, 47, 15, 55, 23, 63, 31,
                38,  6, 46, 14, 54, 22, 62, 30,
                37,  5, 45, 13, 53, 21, 61, 29,
                36,  4, 44, 12, 52, 20, 60, 28,
                35,  3, 43, 11, 51, 19, 59, 27,
                34,  2, 42, 10, 50, 18, 58, 26,
                33,  1, 41,  9, 49, 17, 57, 25,
                32,  0, 40,  8, 48, 16, 56, 24  ]

p_box = [   16,  6, 19, 20, 28, 11, 27, 15,
             0, 14, 22, 25,  4, 17, 30,  9,
             1,  7, 23, 13, 21, 26,  2,  8,
            18, 12, 29,  5, 31, 10,  3, 24  ]

def DES_function(plain_text, key, is_encrypt):
    final_bit_vector = BitVector(size=0)
    round_keys = RoundKey.generate_round_keys(key)
    
    # If decrypting, reverse the round keys
    if not is_encrypt:
        round_keys.reverse()
    
    # Break the plaintext into 64-bit blocks
    plaintext_blocks = [plain_text[i:i+8] for i in range(0, len(plain_text), 8)]
  
    for block in plaintext_blocks:
        block_bit_vector = BitVector(textstring=block)
        
        # Pad with zeros if the length is less than 64
        if len(block_bit_vector) < BLOCK_SIZE: 
            block_bit_vector += BitVector(size=(BLOCK_SIZE - len(block_bit_vector))) 
        
        # Initial permutation
        block_bit_vector = block_bit_vector.permute(initial_permutation_matrix)
        left_half, right_half = block_bit_vector.divide_into_two()

        # 16 rounds of DES
        for round_num in range(16):
            current_round_key = round_keys[round_num]
            # Expansion permutation
            expanded_right_half = right_half.permute(expansion_permutation)
            # XOR with round key
            expanded_right_half = expanded_right_half ^ current_round_key
            # S-Box substitution
            substituted_right_half = S_Box.substitute(expanded_right_half)
            # Permutation
            substituted_right_half = substituted_right_half.permute(p_box)
            # XOR with left half
            new_right_half = substituted_right_half ^ left_half
            # Update halves for next round
            left_half = right_half
            right_half = new_right_half
        
        # Final permutation
        temp_bit_vector = right_half + left_half
        temp_bit_vector = temp_bit_vector.permute(initial_reverse_permutation_matrix)
        final_bit_vector += temp_bit_vector
        
    return final_bit_vector
