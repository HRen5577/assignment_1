import random
from  Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad

#p = 37 #prime number
#g = 5 #primative root

p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5


def relatively_prime(num1):
    temp_prime = p
    temp = -1
    while temp_prime != 0:
         temp = num1
         num1 = temp_prime
         temp_prime = temp % temp_prime

    if num1 == 1:
        return True
    return False


def private_key():
    number = int(random.random()*p)
    
    while relatively_prime(number) == False:
         number = int(random.random()*p)
    
    return number


def public_key(private_key):
    return pow(g,private_key,p)


def person_info(name):
    private = private_key()
    public = public_key(private)
    
    return {
        "name":name,
        "private":private,
        "public":public,
        "secret_key":None,
        "hash_key":None,
    }

    
def generate_key(user_a,user_b):
    return pow(user_b['public'],user_a['private'],p) 

    
def exchange_secret_keys(user_a,user_b):
    user_a['secret_key'] = generate_key(user_a,user_b)
    user_b['secret_key'] = generate_key(user_b,user_a)

    
def generate_hash_key(user_a):
    hash_obj = SHA256.new(bytes(hex(user_a['secret_key']).encode()))
    return hash_obj.digest()


def truncate_hash_key(hash_key):
    return hash_key[:16]
 
 
def hash_keys(user_a,user_b):
    if user_a['secret_key'] != user_b['secret_key']:
        print("Error: Uncommon secret key")
        return False
    
    hash_key = generate_hash_key(user_a) # or generate_hash_key(user_b)
    truncated_hash = truncate_hash_key(hash_key)
        
    user_a["hash_key"] = truncated_hash
    user_b["hash_key"] = truncated_hash
    return True


def encrypt_message(user_a,message,iv):
    cipher = AES.new(user_a['hash_key'], AES.MODE_CBC,iv)
    return cipher.encrypt(message)   
    
def decrypt_message(user_a,message,iv):
    cipher = AES.new(user_a['hash_key'], AES.MODE_CBC,iv)
    return cipher.decrypt(message)   
    
def send_message(user_a,user_b,message):
    iv = get_random_bytes(16)
    print("Message:",message, "sent to ",user_b['name'],"from",user_a['name'] )
    message = pad(message,32)
    message = encrypt_message(user_a,message,iv)
    message = decrypt_message(user_b,message,iv)
    message = unpad(message,32)
    print("Message:",message, "decrypted by",user_b['name'],"from",user_a['name'] )

def main():
    alice = person_info("alice")
    bob = person_info("bob")
    exchange_secret_keys(alice,bob)
    hash_keys(alice,bob)
    send_message(alice,bob,b"Hi Bob")
    send_message(bob,alice,b"Hi Alice")

if __name__ == '__main__':
    main()