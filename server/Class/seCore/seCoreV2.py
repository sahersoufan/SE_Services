from . import names
from . import cleaningHelper 
from ..sqlConnection import dbHandler
from ..embedding import embeddingHandler

import pandas as pd
from traceback import print_exc
import numpy as np


data_frame = None
def initiate():
    """get a hole data and build the recoSys v2 from point zero with new db"""
    try:
        global data_frame
        print('get data from db')
        
        data_frame = pd.read_sql(names.getServiceModel(), con=dbHandler.engine, columns=[names.getJobId(), names.getJobTitle()])
        print('data is here, now we will clean it :)')
        
        data_frame = cleaningHelper.cleanEmbeddingData(data_frame)
        print('data cleanned, building word2vec model...')

        embeddingHandler.initializeModel(data_frame)
        embeddingHandler.makeVectors(data_frame)

    except:
        print_exc()



def update():
    """update the reco system v2 """

    try:
        global data_frame

        print('get data from db')
        
        data_frame = pd.read_sql(names.getServiceModel(), con=dbHandler.engine, columns=[names.getJobId(), names.getJobTitle()])
        print('data is here, now we will clean it :)')
        
        data_frame = cleaningHelper.cleanEmbeddingData(data_frame)
        print('data cleanned, building word2vec model...')

        embeddingHandler.updateModel(data_frame)
        embeddingHandler.makeVectors(data_frame)
    except:
        print_exc()



def getS(userData : dict):
    """get a recommendation"""
    services = {'id' : []}
    global tfidfM, data_frame
    cq = cleaningHelper.cleanStrAdapter(userData.get('title'))
    vectQuery = embeddingHandler.vectQuery(cq)
    result = embeddingHandler.makeCosSim(vectQuery)

    lis:np.ndarray = result.argsort(axis=0)[-50:][::-1]

    for i in lis:
        print(data_frame.iloc[i,0],"--",data_frame.iloc[i,1])
        services.get('id').append(int(data_frame.iloc[i,0]))
    return services