from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np
from ..seCore import names



#variables
tfidf:TfidfVectorizer



def makeTfIdfMatrix(data_frame:pd.DataFrame):
    """
    here we build the tf-idf matrix with TfidfVectorizer from sklear and return the matrix
    """
    try:
        global tfidf
        tfidf = TfidfVectorizer(stop_words='english')
        if data_frame[names.getJobTitle()].isnull().values.any():
            data_frame[names.getJobTitle()] = data_frame[names.getJobTitle()].fillna("")
        tfIdfMatrix = tfidf.fit_transform(data_frame[names.getJobTitle()])
        return tfIdfMatrix, tfidf.vocabulary_
    except:
        print("error in makeTfIdfMatrix() from tfIdfHandler module")
        raise Exception


def updateTfIdfMatrix(data_frame:pd.DataFrame, vocabulary):
    """
    here we update the tf-idf matrix with TfidfVectorizer from sklear and return the matrix
    """
    try:
        global tfidf
        tfidf = TfidfVectorizer(stop_words='english', vocabulary=vocabulary)
        if data_frame[names.getJobTitle()].isnull().values.any():
            data_frame[names.getJobTitle()] = data_frame[names.getJobTitle()].fillna("")
        tfIdfMatrix = tfidf.fit_transform(data_frame[names.getJobTitle()])
        return tfIdfMatrix, tfidf.vocabulary_
    except:
        print("error in updateTfIdfMatrix() from tfIdfHandler module")
        raise Exception

def vectQuery(query):
    global tfidf
    return tfidf.transform([query])


def makeCosSim(tfidfMatrix, query) -> np.ndarray:
    """ build a table of cosine similarity from the tf idf matrix with query"""
    cosine_sim = linear_kernel(tfidfMatrix, query)
    return cosine_sim




# def makeJobsIndices(data : pd.DataFrame):
#     """make indices from ids"""
#     indicies = pd.DataFrame(data=data['id'])
#     indicies.rename(columns={'id':'jobsId'}, inplace=True)
#     indicies['simId'] = indicies.index.values
#     indicies.set_index('jobsId', inplace=True)
#     return indicies

