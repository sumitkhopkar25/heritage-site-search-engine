import pickle
import math
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PIL import Image
import requests
from io import BytesIO

def read_dict():
    dict_file = open("E:\Important\Study_Material\CA6005\Project 2\\tf_idf_dict.pkl", "rb")
    token_dict = pickle.load(dict_file)
    
    dict_file = open("E:\Important\Study_Material\CA6005\Project 2\herit_dict.pkl", "rb")
    herit_dict = pickle.load(dict_file)
    
    dict_file = open("E:\Important\Study_Material\CA6005\Project 2\\sim_img_dict.pkl", "rb")
    sim_img_dict = pickle.load(dict_file)
    
    return(token_dict, herit_dict, sim_img_dict)

def fetch_query(conc_str):
    token_dict, herit_dict, sim_img_dict = read_dict()
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    no_pun_str = conc_str.translate(str.maketrans('', '', string.punctuation))
    word_tokens = word_tokenize(no_pun_str)
    filtered_sentence = [lemmatizer.lemmatize(w.lower()) for w in word_tokens if not w.lower() in stop_words]
    fil_sent_dict = {}

    for word in filtered_sentence:

        if word in fil_sent_dict:
            fil_sent_dict[word] += 1
        else:
            fil_sent_dict[word] = 1
            
    word_norm = 0

    for word in fil_sent_dict:
        word_norm = word_norm + fil_sent_dict[word]*fil_sent_dict[word]

    fil_sent_dict['word_norm_q'] = math.sqrt(word_norm)
        
    query = fil_sent_dict
    
    rank = cos_sim(token_dict, query)
    
    sim_img_list = []
    
    for link in sim_img_dict[rank[0][0]]:
        sim_img_list.append(link)
                
    return rank, herit_dict, sim_img_list

#Function to calculate cosin similarity
def cos_sim(token_dict, query):
    rank = {}
    cnt = 0
    
    query_word_norm = query['word_norm_q']
    
    for doc in token_dict:
        if(cnt < 30000000):
            numer = 0
            denom = 0
            
            for word in query:
                #If query term is present in the document then calculate dot product or else dot product becomes zero
                if word in token_dict[doc]:
                    dot_prod = query[word]*token_dict[doc][word]['tf_idf']
                else:
                    dot_prod = 0
                    
                numer += dot_prod
                
            denom = token_dict[doc]['word_norm_c']*query_word_norm #Multiply the term norms to form the denominator
            cosin = numer/denom #Cosin similarity

            rank[doc] = cosin
            
            cnt += 1
            
    rank = sorted(rank.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)[0:10]

    return(rank)

def ret_img(rank, herit_dict):
    
    final_res = []
        
    for herit in rank:
        img_link = "https:" + herit_dict[herit[0]]['img_link']
        desc = herit_dict[herit[0]]['desc']
        final_res.append({'herit':herit[0], 'img': img_link, 'desc': desc})
        
    return final_res

def caller(conc_str):
    rank, herit_dict, sim_img_list = fetch_query(conc_str)
    img_list = ret_img(rank, herit_dict)
    result = {}
    result['data'] = img_list
    result['images'] = sim_img_list
    return result

#if __name__ == "__main__":
   #result = caller('mountain')
   #print(result['images'])
