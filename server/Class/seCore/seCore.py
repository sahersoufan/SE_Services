from json import load
from logging import exception
from unittest import result
import numpy as np
import pandas as pd
import pickle
import os
from . import cleaningHelper
from ..sqlConnection import dbHandler
from ..tfIdf import tfIdfHandler
from . import names

#variables#
# cosSim:np.ndarray = None
# indicies:pd.DataFrame = None
tfidfM = None
data_frame = None



def setSqlInfo(info:dict):
    '''initialize sql connection information '''
    dbHandler.setSqlInfo(info)




def initiate():
    """get a hole data and build the recoSys from point zero with new db"""
    try:
        print('get data from db')
        global tfidfM, data_frame
        data = pd.read_sql('jobs', con=dbHandler.engine, columns=[names.getJobId(), names.getJobTitle()])

        data_frame = pd.DataFrame(data)
        print('data is here, now we will clean it :)')
        
        data_frame = cleaningHelper.cleanData(data_frame)
        print('data cleanned, building tfidf matrix')

        tfidfM = tfIdfHandler.makeTfIdfMatrix(data_frame=data_frame)
        print('tfidf matrix is here, now we build cosin similarity and indicies')
        
    
        # if(os.path.exists(os.path.join(os.getcwd(), names.getVoc()))):
        #     os.remove(os.path.join(os.getcwd(), names.getVoc()))
        # pickle.dump(voc, open(os.path.join(os.getcwd(), names.getVoc()), "wb"))
        # print('saving is done')
    except:
        print('error in initiate func')
        raise exception

def update():
    """update the reco system """
    try:
        global tfidfM, data_frame
        print('get data from db')
        data = pd.read_sql('jobs', con=dbHandler.engine, columns=[names.getJobId(), names.getJobTitle()])
        data_frame = pd.DataFrame(data)
        print('data is here, now we will clean it :)')
        
        data_frame = cleaningHelper.cleanData(data_frame)
        print('data cleanned, building tfidf matrix')
        savedVocabulary = pickle.load(open(os.path.join(os.getcwd(), names.getVoc()), "rb"))
        tfidfM,voc = tfIdfHandler.updateTfIdfMatrix(data_frame=data_frame, vocabulary=savedVocabulary)
        print('tfidf matrix is here, now we build cosin similarity and indicies')


        if(os.path.exists(os.path.join(os.getcwd(), names.getVoc()))):
            os.remove(os.path.join(os.getcwd(), names.getVoc()))
        pickle.dump(voc, open(os.path.join(os.getcwd(), names.getVoc()), "wb"))
        print('saving is done')
        return 0
    except:
        print('error in update func')
        raise exception



def getS(userData : dict):
    """get a recommendation"""
    services = {'id' : []}
    global tfidfM, data_frame
    vectQuery = tfIdfHandler.vectQuery(userData.get('title'))
    result = tfIdfHandler.makeCosSim(vectQuery, tfidfM)

    lis:np.ndarray = result.argsort(axis=0)[-50:][::-1]
    services.get('id').append(lis.tolist())
    for i in lis:
        print(data_frame.iloc[i,0],"--",data_frame.iloc[i,1])
    return services


