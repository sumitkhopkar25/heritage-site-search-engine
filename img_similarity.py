import pickle
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity_cosine(vector1, vector2):
    #return 1- distance.cosine(vector1, vector2)
    return cosine_similarity(vector1, vector2) 

def save_dict(sim_img_dict):
    try:
        sim_img_dict_file = open('E:\Important\Study_Material\CA6005\Project 2\sim_img_dict.pkl', 'wb')
        pickle.dump(sim_img_dict, sim_img_dict_file)
        sim_img_dict_file.close()

    except:
        print("Something went wrong")

dict_file = open("E:\Important\Study_Material\CA6005\Project 2\herit_dict.pkl", "rb")
herit_dict = pickle.load(dict_file)

img_dict_file = open("E:\Important\Study_Material\CA6005\Project 2\\feat_img_dict.pkl", "rb")
feat_img_dict = pickle.load(img_dict_file)

sim_img_dict = {}

for herit in feat_img_dict:
        sim_img_dict[herit] = {}

        for img_feat in feat_img_dict:

                if(img_feat != herit):
                    vector1 = feat_img_dict[herit]
                    vector2 = feat_img_dict[img_feat]
                    sim_img_dict[herit][img_feat] = calculate_similarity_cosine(vector1, vector2)[0][0]
        sim_img_dict[herit] = sorted(sim_img_dict[herit].items(), key = lambda kv:(kv[1], kv[0]), reverse = True)[0:10]
        
for herit in sim_img_dict:
    sim_img_dict[herit] = [name[0] for name in sim_img_dict[herit]]
    
for herit in sim_img_dict:
    sim_img_dict[herit] = [herit_dict[name]['img_link'] for name in sim_img_dict[herit]]
    
save_dict(sim_img_dict)