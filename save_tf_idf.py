import pickle
import math

#Read the dictionary stored as metadata for tokens and words
def read_dict(dict_type):

    if(dict_type == 'token'):
        dict_file = open("E:\Important\Study_Material\CA6005\Project 2\\token_dict.pkl", "rb")
        output = pickle.load(dict_file)
    else:
        dict_file = open("E:\Important\Study_Material\CA6005\Project 2\word_dict.pkl", "rb")
        output = pickle.load(dict_file)
    
    return(output)

def save_tf_idf(token_dict, word_dict):
    cnt = 0
    doc_num = len(token_dict.keys())

    for doc in token_dict:
        if(cnt < 30000000000):
            word_norm = 0 #Norm of the term frequencies
            
            for word in token_dict[doc]:
    
                #doc_len and avgdl are stored as keys in the same level as that of words in the tokens dict
                if(word != 'doc_len' and word != 'avgdl'):
                    occur = token_dict[doc][word]
                    occur_all = word_dict[word]['occur_all']
                    doc_freq = word_dict[word]['doc_freq']
                    tf = occur/occur_all #Formula for tf
                    idf = math.log(doc_num/doc_freq) #Formula for idf
                    tf_idf = tf*idf
                    word_norm = word_norm + tf_idf*tf_idf
                    token_dict[doc][word] = {}
                    token_dict[doc][word]['tf_idf'] = tf_idf
                    
            token_dict[doc]['word_norm_c'] = math.sqrt(word_norm)
            
            cnt += 1
            print(cnt)
            
    return(token_dict)

def save_dict(token_dict):

    try:
        token_dict_file = open('E:\Important\Study_Material\CA6005\Project 2\\tf_idf_dict.pkl', 'wb')
        pickle.dump(token_dict, token_dict_file)
        token_dict_file.close()

    except:
        print("Something went wrong")

def main():
    token_dict = read_dict('token')
    word_dict = read_dict('word')
    token_dict = save_tf_idf(token_dict, word_dict)
    save_dict(token_dict)

if __name__ == "__main__":
    main()