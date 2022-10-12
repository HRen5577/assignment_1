from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def read_header(in_file,out_file):
    # Read in the header to the encrypted file
    out_file.write(in_file.read(54))


def read_data_ecb(key,in_file):
    atEnd = False
    cipher = AES.new(key, AES.MODE_ECB)

    data = in_file.read(16)
    ciphertext = cipher.encrypt(data)
    
    while atEnd == False and len(data) == 16:
        data = in_file.read(16)
        
        if(len(data) < 16):
            num = 16 - len(data)            
            data += num.to_bytes(1,'big') * num
            atEnd = True
                    
        ciphertext += cipher.encrypt(data)

    return ciphertext


def read_data_cbc(key,iv,in_file):
    atEnd = False
    cipher = AES.new(key, AES.MODE_ECB)

    data = in_file.read(16)
    data =  bytes([_a ^ _b for _a, _b in zip(data, iv)])
    ciphertext = cipher.encrypt(data)
    
    
    while atEnd == False and len(data) == 16:
        old_data = data
        data = in_file.read(16)
        
        if(len(data) < 16):
            num = 16 - len(data)            
            data += num.to_bytes(1,'big') * num
            atEnd = True
        
        data  =  bytes([_a ^ _b for _a, _b in zip(data, old_data)])    
        ciphertext += cipher.encrypt(data)

    return ciphertext

def read_to_output(cipher_text,file_out):    
    for item in cipher_text:
        file_out.write(item.to_bytes(1,'big'))

def ecb_encryption():
    key = get_random_bytes(16)
    image_data = open("mustang.bmp","rb")# 54 bytes for header or 138 bytes
    file_out = open("mustand_enc.bmp", "wb")

    read_header(image_data,file_out)
    cipher_text = read_data_ecb(key,image_data)
    read_to_output(cipher_text,file_out)
    
    image_data.close()
    file_out.close()
    

def cbc_encryption():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    image_data = open("assignment1\cp-logo.bmp","rb")# 54 bytes for header or 138 bytes
    file_out = open("assignment1\cp_logo_enc.bmp", "wb")

    print(key)
    print(type(key))

    read_header(image_data,file_out)
    cipher_text = read_data_cbc(key,iv,image_data)
    read_to_output(cipher_text,file_out)
    
    image_data.close()
    file_out.close()
    
def main():
    ecb_encryption()
    cbc_encryption()


if __name__ == '__main__':
    main()