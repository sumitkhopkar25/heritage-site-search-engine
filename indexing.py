import pickle
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

dict_file = open("E:\Important\Study_Material\CA6005\Project 2\herit_dict.pkl", "rb")
herit_dict = pickle.load(dict_file)
tokens = {}
word_dict = {}

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

cnt = 0

def save_dict():
    try:
        token_dict_file = open('E:\Important\Study_Material\CA6005\Project 2\\token_dict.pkl', 'wb')
        pickle.dump(tokens, token_dict_file)
        token_dict_file.close()

        word_dict_file = open('E:\Important\Study_Material\CA6005\Project 2\word_dict.pkl', 'wb')
        pickle.dump(word_dict, word_dict_file)
        word_dict_file.close()
  
    except:
        print("Something went wrong")

for herit in herit_dict:
    if(cnt < 30000000):
        conc_str = herit + " " + herit_dict[herit]['continent'] + " " + herit_dict[herit]['country'] + " " + herit_dict[herit]['desc']
        no_pun_str = conc_str.translate(str.maketrans('', '', string.punctuation)) #Remove punctuations
        word_tokens = word_tokenize(no_pun_str) #Tokenize the string
        filtered_sentence = [lemmatizer.lemmatize(w.lower()) for w in word_tokens if not w.lower() in stop_words] #Stem the words
        fil_sent_dict = {}
        
        for word in filtered_sentence:
            
            #Calculate term frequency
            if word in fil_sent_dict:
                fil_sent_dict[word] += 1
            else:
                fil_sent_dict[word] = 1
    
            #Calculate the term frequency in the entire collection
            if word in word_dict:
                word_dict[word]['occur_all'] += 1
            else:
                word_dict[word] = {}
                word_dict[word]['occur_all'] = 1
                
        tokens[herit] = fil_sent_dict
        tokens[herit]['doc_len'] = len(fil_sent_dict)
        #tokens[herit]['doc_words_len'] = sum(fil_sent_dict.values())
        
        for word in set(filtered_sentence):
            #Calculate and store document frequency for the term
            if 'doc_freq' in word_dict[word]:
                word_dict[word]['doc_freq'] += 1
            else:
                word_dict[word]['doc_freq'] = 1
        
        cnt += 1
        print(cnt)

save_dict()
#print(word_dict)