from audioop import avg
from glob import glob
from statistics import mode
from traceback import print_exc
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import os

from sklearn.metrics.pairwise import cosine_similarity
from ..seCore import names


model = None
vectors = []
cosineSimilarity = None

def initializeModel(dataFrame:pd.DataFrame()):
    global model
    try:
        corpus = []
        for words in dataFrame[names.getJobTitle()]:
            corpus.append(words.split())
            
        model = Word2Vec(
            sentences= corpus,
            vector_size=300,
            workers=4
        )
        if os.path.exists('word2vec.model'):
            os.remove('word2vec.model')
        model.save('word2vec.model')
    except:
        print_exc()


def updateModel(dataFrame:pd.DataFrame()):
    try:
        if model is None or not os.path.exists('word2vec.model'):
            initializeModel(dataFrame)
            return
        
        model = Word2Vec.load('word2vec.model')
        model.build_vocab(dataFrame[names.getJobTitle()], update = True)
        
        corpus = []
        for words in dataFrame[names.getJobTitle()]:
            corpus.append(words.split())

        model.train(
            corpus,
            total_examples = model.corpus_count,
            epochs = model.epochs
        )

        os.remove('word2vec.model')
        model.save('word2vec.model')

    except:
        print_exc()


def makeVectors(dataFrame:pd.DataFrame()):
    global vectors
    try:
        te = dataFrame[names.getJobTitle()]
        tc =0
        for line in te:
            avgword2vec = None
            count=0
            for word in line.split():

                if word in model.wv:
                    count+=1
                    if avgword2vec is None:
                        avgword2vec  =model.wv[word]
                    else:
                        avgword2vec =avgword2vec + model.wv[word]

            if avgword2vec is not None:
                avgword2vec = avgword2vec / count

                vectors.append(avgword2vec)
            else:
                vectors.append([0]*300) 
        print(len(te), len(vectors))
        
    except:
        print_exc()



def vectQuery(query:str):
    try:
            avgword2vec = None
            count=0
            for word in query.split():
                if word in model.wv:
                    count+=1
                    if avgword2vec is None:
                        avgword2vec  =model.wv[word]
                    else:
                        avgword2vec =avgword2vec + model.wv[word]

            if avgword2vec is not None:
                avgword2vec = avgword2vec / count

                return [avgword2vec]
    except:
        print_exc()




def makeCosSim(query) -> np.ndarray:
    """ build a table of cosine similarity from the tf idf matrix with query"""
    global vectors
    cosine_sim = cosine_similarity(query, vectors).flatten()
    return cosine_sim
