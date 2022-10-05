from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


equals_CODE = "%3D"
semi_colon_CODE = "%3B"


def ask_user():
    print("Enter some user data: ")
    return input()

def url_encode(data):
    data = data.replace("=", equals_CODE)
    return data.replace(";", semi_colon_CODE )


def url_decode(data):
    data = data.replace(equals_CODE,"=")
    return data.replace(semi_colon_CODE,";" )


def pad_data(data):
    data = bytes(data)
    n = 16-len(data)%16

    data += n.to_bytes(1,'big')*n
    return data


def unpad_data(data):
    count = 0
    rev_text = data[::-1]

    int_padding = int(rev_text[0])
    
    for i in range(1,16):
        if int_padding == int(rev_text[i]):
            count += 1
        else:
            break

    if count == int_padding-1:
        return (rev_text[count+1:len(rev_text)])[::-1]


def isAdmin(data):
    if data.find(";admin=true;") != -1:
        return True
    return False


def encrypt_data(key,iv,data):
    cipher = AES.new(key, AES.MODE_ECB)
    
    plain_text = data[0:16]
    xor_text = bytes([_a ^ _b for _a, _b in zip(plain_text, iv)])
    encrypted_text = cipher.encrypt(xor_text) 
    ciphertext =    encrypted_text

    range_end = (len(data)//16)
    for i in range(1,range_end):
        old_encrypted_text = encrypted_text
        plain_text = data[(i*16):(i*16)+16]        
        xor_text  =  bytes([_a ^ _b for _a, _b in zip(plain_text, old_encrypted_text)])    
        encrypted_text = cipher.encrypt(xor_text) 
        ciphertext +=    encrypted_text 
    return ciphertext


def decrypt_data(key,iv,data):
    cipher = AES.new(key, AES.MODE_ECB)

    ciphertext = data[0:16]    
    xor_text = cipher.decrypt(ciphertext)
    text =  bytes([_a ^ _b for _a, _b in zip(xor_text,iv)])
        
    range_end = (len(data)//16)
    for i in range(1,range_end):
        old_ciphertext = ciphertext
        ciphertext = data[(i*16):(i*16)+16]
        xor_text = cipher.decrypt(ciphertext)
        
        text  +=  bytes([_a ^ _b for _a, _b in zip(xor_text,old_ciphertext)])    

    return text
      

def submit(key,iv):
    user_data = ask_user() #"aadmin[true" 
    user_data = url_encode(user_data)
    data = "userid=156;userdata={};session-id=31337".format(user_data)
    data = data.encode('latin-1')
    data = pad_data(data)
    print(data)
    return encrypt_data(key,iv,data)


def verify(key,iv,data):
    data = decrypt_data(key,iv,data)
    data = unpad_data(data)
    data = data.decode('latin-1')
    print(data)
    return isAdmin(data)


def bitflip(cipher_text):
    #Bit Flip
    
    c1_no = cipher_text[:4]
    c1 = cipher_text[4]
    c1 =  (c1 ^ ord("a".encode("latin-1")) ^ ord(";".encode("latin-1"))).to_bytes(1,"big")

    c2_no = cipher_text[5:10]
    c2 = cipher_text[10]
    c2 = (c2 ^ ord("[".encode("latin-1")) ^ ord("=".encode("latin-1"))).to_bytes(1,"big")
    
    c3 = cipher_text[11:]
    
    c1_no += c1
    c1_no += c2_no
    c1_no += c2
    c1_no += c3

    return c1_no


def main():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    
    cipher_text = submit(key,iv)
    bitflip_text = bitflip(cipher_text)
    verified = verify(key,iv,bitflip_text)
    print(verified)


if __name__ == '__main__':
    main()