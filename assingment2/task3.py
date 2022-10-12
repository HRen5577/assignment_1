from math import gcd
import random
from re import A
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from Crypto.Util.number import getPrime,inverse
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad,unpad
from Crypto.Util.number import GCD
####################################
########### RSA ####################


def pick_bits():
    print("What is your bit size (has to be a multple of 128)")
    bits = -1
    ans = ""
    
    bits = int(input())
    while ans != "y":
        
        if bits % 128 == 0 and bits < 2049:
            return bits
        
        print("What is your bit size (has to be a multple of 128)")
        bits = int(input())
    
    return bits
    

def user_info(name,bits):
    e = 65537

    if bits == None:
        bits = 128
    
    p = getPrime(bits) #17getStrongPrime(bits,e)
    q = getPrime(bits) #11getStrongPrime(bits,e)
    
    n = p * q #187
    
    euler_totient = (p-1) * (q-1) #160
    
    d = inverse(e,euler_totient)#23
    
    return {
        "name":name,
        "public":(e,n),
        "private":(d,n)
    }


def send_public_key(user_a,user_b):
    key_name = user_a['name'] + "_public"
    user_b[key_name] = user_a['public']


def encrypt_message(public_key,message):
    e = public_key[0]
    n = public_key[1] 
    
    message = message.encode('latin-1')

    if len(message) > n:
        return False

    message = message.hex()
    message = int(message,16)
    message = pow(message,e,n)
    
    return hex(message)


def send_key(user_a,user_b):
    key = user_b['name'] + "_scret_key"
    user_a[key] = user_b['secret_key']


def decrypt_message(private_key,message,message_len):
    d = private_key[0]
    n = private_key[1]

    message = int(message,16)
    message = pow(message,d,n)
    message = message.to_bytes(message_len,'big')
    message = message.decode()
        
    return message


def rsa_message(user_a,message):
    message_len = len(message)
    
    print("Message: '",message,"' encrypted by",user_a['name'])
    message = encrypt_message(user_a['public'],message)
    print("Message encrypted to",message)
    message = decrypt_message(user_a['private'],message,message_len)
    print("Message: '",message,"' decrypted by",user_a['name'])


def part1():
    #bits = pick_bits()
    bits = 128
    alice = user_info('alice',bits)
    bob = user_info('bob',bits)
    
    rsa_message(alice,"Hello me")
    print()
    rsa_message(bob,"Hello Alice, How are you")


####
# ----- Part 2 -----
####


def user_info_part2(name, n):
    e = 65537
    p = int(random.random() * n)

    while int(gcd(p,n)) != 1:
        p = random.random() * n
    
    cipher_text = pow(p,e,n)
    return {
        "name":name,
        "cipher_text": cipher_text,
        "secret_key":p
    }
    
    
def intercept_secret(user_a,user_b,user_c):
    # Ignore the old cipher text
    old_cipher_text = user_b['cipher_text']
    
    if user_a == None:
        u = user_info_part2(user_c['name'],1)    
    else:
        u = user_info_part2(user_c['name'],user_a['public'][1])
    return u


def send_secret_key(user_a,user_b):    
    user_a["cipher_text"] = user_b['cipher_text']
    user_a['secret_key'] = pow(user_a['cipher_text'],user_a['private'][0],user_a['private'][1])


def generate_hash_key(user_a):
    hash_obj = SHA256.new(bytes(hex(user_a['secret_key']).encode()))
    return hash_obj.digest()


def hash_keys(user_a,user_b):
    user_a['hash_key'] = generate_hash_key(user_a)[:16]
    user_b['hash_key'] = generate_hash_key(user_b)[:16]
    pass

def send_secret_key_message(user_a,user_b,user_c,message):
    iv = user_a['hash_key']
    print("Message:",message, "sent to ",user_b['name'],"from",user_a['name'] )
    message = pad(message,32)
    message = encrypt_message_part2(user_a,message,iv)
    print("Message encrpted to:",message)
    message = decrypt_message_part2(user_c,message,iv)
    message = unpad(message,32)
    print("Message:",message, "was intercepted and decrypted by",user_c['name'],"from",user_a['name'] )



def encrypt_message_part2(user_a,message,iv):
    cipher = AES.new(user_a['hash_key'], AES.MODE_CBC,iv)
    return cipher.encrypt(message)   
    
def decrypt_message_part2(user_a,message,iv):
    cipher = AES.new(user_a['hash_key'], AES.MODE_CBC,iv)
    return cipher.decrypt(message)   


#######
# Signature
######

def signature(message,private_key):
    d = private_key[0]
    n = private_key[1]
    return pow(message,d,n)


def decrypt_sig(sig,public):
    e = public[0]
    n = public[1]
    return pow(sig,e,n)    


def part2():
    alice = user_info("alice",128)
    bob = user_info_part2("bob",alice['public'][1])
    mallory = user_info_part2("mallory",alice['public'][1])
    mallory = intercept_secret(alice,bob,mallory)
    send_secret_key(alice,mallory)
    hash_keys(alice,mallory)
    send_secret_key_message(alice,bob,mallory,b"Hello Bob")

def message():
    m1 = 2
    m2 = 4
    m3_1 = m1 * m2
    
    alice = user_info("alice",128)
    sig1 = signature(m1,alice['private'])
    sig2 = signature(m2,alice['private'])

    sig3 = (sig1*sig2) % alice['public'][1]
    m3_2 = decrypt_sig(sig3,alice['public'])

    print("sig1",sig1,"sig2",sig2)
    print("sig3",sig3)
    
    print("They are the same message",m3_1==m3_2)
    
def main():
    # Comment out the part that want to see
    print("---------- Part 1 -----------------")
    part1()
    print("---------- END -----------------")
    print("---------- Part 2 -----------------")
    part2()
    print("---------- END -----------------")

    #message()
    
    
if __name__ == '__main__':
    main()