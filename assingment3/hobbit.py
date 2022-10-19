
def wordList():
    all_words = []
    with open('hobbit.txt', encoding="utf8") as f:
        for line in f:
            words = line.split(" ")
    
            for word in words:
                word = word.replace("\n","")
                word = word.replace("\'","")
                word = word.replace("\"","")
                word = word.replace(".","")
                word = word.replace(";","")
                word = word.replace(":","")
             
                all_words.append(word)
                #print(set(all_words))
    return set(all_words)
