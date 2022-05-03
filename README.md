# Search Engine for World Heritage Sites

This project provides a search engine UI and its back-end components to lookup any heritage site in the world with its image and description. The images have been crawled from Wikipedia along with their descriptions. I could crawl through 1073 out of a total of 1154 heritage sites of irregularities in the webpage structure of the heritage sites which I couldn't crawl. This is how the layout of the search page looks like -

![image](https://user-images.githubusercontent.com/63579785/166454442-58a5a852-067f-4832-9aca-b6b59ea47cb0.png)

This is how the search result looks like -

![image](https://user-images.githubusercontent.com/63579785/166454461-d8871df6-40a1-4906-9d85-ad0a6c0d1af0.png)

The search result provides the 10 most relevant results obtained from the search query. The search mechanism makes use of Cosine Similarity algorithm to fetch the topmost ranked results to the search query. The search query can be vague as well such as "Ocean", "Desert" and the heritage sites which are the most appropriate are retrieved.

Another feature available is to view the images that are the most "visually similar" to the topmost heritage site retrieved.

# Table of Contents
* [Installation](https://github.com/sumitkhopkar25/heritage-site-search-engine/tree/main#installation)
* [Usage](https://github.com/sumitkhopkar25/heritage-site-search-engine/tree/main#usage)
* [Development](https://github.com/sumitkhopkar25/heritage-site-search-engine/tree/main#development)
* [Acknowledgments](https://github.com/sumitkhopkar25/heritage-site-search-engine/tree/main#acknowledgments)

# Installation
Before using the website some steps need to be followed to create the dictionary of indexes of words which allow the search query to fetch the most relevant heritage site. The codes need to be run in the below sequence before running the website -

## Create index of textual surrogates
1. crawler.py
2. indexing.py
3. save_tf_idf.py

## Create dictionary of most visually similar images
1. make_feature_vectors.py
2. img_similarity.py

This is done to save as much metadata as we can to reduce latency at run-time while the search result is being fetched. Before running these codes please change the filepaths local to your file system. 

Other than the regular Data Science and nltk Python libraries which you would need to install you would also need to download the corpus of nltk's stopwords (English). This can be done by opening a Python terminal and running the below code -

```
import nltk
nltk.download()
```

# Usage
On running the above codes and saving the required metadata, the file main.py should be run using Python's flask library. In a command prompt run the below commands -

```
set FLASK_APP=main
flask run
```

Navigate to the localhost IP address and default port (which is by default http://127.0.0.1:5000/) to open the website.

# Development
The crawler code can be improved to handle all exceptions, since currently not all heritage sites are being able to be fetched. Also, the description section is not correct for the heritage sites of some countries such as India, China and the U.S. More Language Models can be tried out in place of Vector Space Model. If another language model is used then even the TF-IDF code would need to be changed since indexing is different for different retrieval algorithms. 

# Acknowledgments
The code to find the most visually similar images is acquired from the following github repository -

https://github.com/XingLiangLondon/Image-Similarity-in-Percentage
