import random
import time
from Crypto.Hash import SHA256


def word_to_bits(word):
    return ''.join(format(ord(i), '08b') for i in word)


def hamming_distance(word1,word2):
    word1_bits = word_to_bits(word1)
    word2_bits = word_to_bits(word2) 
    
    print(word1,"bit string is:",word1_bits)
    print(word2,"bit string is:",word2_bits)
  
  
    
def hash_input(word):
    return SHA256.new(word.encode("ascii"))


def truncate_hash(given_hash,bytes_length):
    return given_hash[:bytes_length]


def part_a(word):
    print("---------------- Part A -------------------")
    hash_obj = hash_input(word)    
    print(word,"hashed to:",hash_obj.hexdigest())
    print(word,"truncated hash to:",truncate_hash(hash_obj.hexdigest(),2))
    print("---------------- END -------------------")

    
def part_b(word1,word2):
    print("---------------- Part B -------------------")
    hamming_distance(word1,word2)
    print("---------------- END -------------------")


def random_word(bytes_length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuwxyz1234567890-=+_)(*&^%$#@!,./?><';:][\|"
    
    word = ""
    word = ''.join(random.choices(alphabet, k=bytes_length))
    
    #time.time()
    # for i in range(bytes_length):
    #     index = int((random.random() * len(alphabet)))
    #     word += alphabet[index]
    
    return word

def truncate_bits(bits_need,bits_have):
    word = random_word(bits_have//8)
    word_bits = word_to_bits(word)
    word_truncated = word_bits[:bits_need]
    
    return word_truncated


def part_c():
    print("---------------- Part C -------------------")
    f = open("info.csv", "w")
    f.write("bits,time,total_inputs") 
    f.write("\n")
    
    for i in range(1,26):
        total_bits_seen = []
        total_dict = {}
        
        start_time = time.time()

        total_inputs = 0
        
        current_bits = i*2
        collision = False

        while collision == False:
            current_word1 = random_word(int(random.random()*32)+1)
            
            # if current_bits % 8 == 0:
            #     current_word1 = random_word(current_bits//8)
            # else:
            bits_need = current_bits + (8 - (current_bits%8))  
            #     current_word1 = random_word(bits_need//8)
            
            total_inputs += 1

            #bits_need = current_bits + ( 8-(current_bits%8) )
            hash_obj1 = hash_input(current_word1)
            truncated1 = truncate_hash(hash_obj1.hexdigest(),bits_need)
            bits_string1 = (bin(int(truncated1, 16))[2:].zfill(bits_need))[:current_bits]
            
            bits_int = int(bits_string1,2)

            if bits_int in total_dict and total_dict[bits_int] != current_word1:
                end_time = time.time()
                total_time = end_time - start_time

                print("-------------------------")
                print("Collison Found!")
                print("Word Seen:",total_dict[bits_int])
                print("Word Picked Currently:",current_word1)
                print("Bits:",current_bits)
                print("Total inputs:",total_inputs)
                print("Total Time:",total_time)
                print("-------------------------")
                string = f"{current_bits},{total_time},{total_inputs}"
                f.write(string)
                f.write("\n")
                collision = True
                total_inputs = 0
            elif bits_int not in total_bits_seen:
                total_dict[bits_int] = current_word1
                
                
        collision = False
    print("---------------- END -------------------")
    f.close()
    
if __name__ == "__main__":
    input_word = "hello world"
    word1 = "hello"
    word2 = "hellm"

    #part_a(input_word)
    #part_b(word1,word2)
    part_c()
