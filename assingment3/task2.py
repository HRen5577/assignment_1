from math import fabs
import bcrypt
import random
from nltk.corpus import words
import time
import concurrent.futures

def get_hash_string(entire_string):
    
    index = 0
    for i in range(len(entire_string)):
        if entire_string[i] == ":":
            index = i

    return (entire_string[:index],entire_string[index+1:])


def seperate_info(hash_string):
    info = hash_string.split("$")
    salt = ("$" + info[1] + "$" + info[2] + "$" + info[3][:22]).encode()

    return (info[0],info[1],salt,info[3][22:len(info[3])-1])


def generate_person_info(user_line):
    username, hash_string = get_hash_string(user_line)
    algorithm, workfactor, salt,hash = seperate_info(hash_string)

    return {
        "name":username,
        "algorithm":algorithm,
        "workfactor":workfactor,
        "salt": salt,
        "hash":hash
    }


def validate_hash(user,password):
    
    hashed_line = bcrypt.hashpw(password,user["salt"])
    hash_start = len(user["algorithm"]) + len(user['workfactor']) + 3 + 24
    hash = hashed_line.decode()[hash_start:]

    if hash == user['hash']:
        return True
    else:
        return False


def generate_name(length):
    alphabet = "ABCDEFGHIJKLMOPQRSTUVWVYZabcdefghijklmnopqrstuvwxyz1234567890"

    name = ""
    for i in range(length):
        index = int(random.random() * len(alphabet))
        letter = alphabet[index]
        name += letter
    return name


def get_users():
    users = []
    with open(".\\assingment3\\passwords.txt","r") as f:
            for user_line in f:
                users.append(user_line)
    return users


def get_user_compiled(users):
    user_dict = {}
    
    for user in users:
        user_info = generate_person_info(user)
        user_dict[user_info['name']] = user_info
        
    return user_dict

def seperate_possible_passwords(l): 
    amount = len(l)//100

    complete_list = []
    for i in range(100):
        if i == 99:
            new_list = l[amount*i:(i*amount)+amount+(amount%100)]
        else:
            new_list = l[amount*i:(i*amount)+amount]
        complete_list.append(list(new_list))
    
    return complete_list

def check_word(user, word):
        
    hashed_line = bcrypt.hashpw(word.encode('utf-8'),user["salt"])
    hash_start = len(user["algorithm"]) + len(user['workfactor']) + 3 + 24
    hash = hashed_line.decode()[hash_start:]

    if hash == user['hash']:
        return word
    
    return None

def find_passwords():
    users = get_users()
    user_dict = get_user_compiled(users)

    file = open("cracked_passwords.txt","w")
    file.write("name,password,time\n")
    
    
    
    for user in user_dict:
        start_time = time.time()
        all_words = list(set(words.words()))
        all_words = list(filter(lambda word: len(word) >=6 and len(word) <=10, all_words))
   
        all_words = seperate_possible_passwords(all_words)

        found = False
        for wordList in all_words:
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                # Start the load operations and mark each future with its URL
                total_responses = {executor.submit(check_word, user_dict[user], word): word for word in wordList}
                
                for future in concurrent.futures.as_completed(total_responses):
                    url = total_responses[future]
                    
                    try:
                        data = future.result()
                        if data != None:
                            end_time = time.time()
                            total_time = end_time - start_time
                            print(user, ":",data,"took",total_time)  
                            line = str(user + "," + str(data) + "," + str(total_time))
                            file.write(line)
                            file.write("\n") 
                            found = True 
                    except Exception as exc:
                        pass
                        #print('%r generated an exception: %s' % (url, exc))
                    else:  
                        pass
                        #print("Something happened")
            if found == True:
                break

    file.close()


def main():
    #generate_test_file()
    find_passwords()

main()

