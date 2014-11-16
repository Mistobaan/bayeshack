import pandas as pd
import numpy as np
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.lda import LDA
from sklearn.cluster import KMeans,MiniBatchKMeans
import pickle
from api.helper import race,raceapply2
from sklearn.neighbors import NearestNeighbors

def get_head(x):
    return(x.head(1))
#data=pd.read_table("escort_all.tsv")
#data.reindex(np.random.permutation(data.index))
#data.to_csv("unsorteddata.csv",index=False)
data=pd.read_csv("unsorteddata.csv",nrows=500000)
data=data[['postTitle','postText','City','Location']]
data=data[(pd.isnull(data['postTitle'])==False) & (pd.isnull(data['postText'])==False)]
data['race1']=data['postTitle'].map(race)
data['race2']=data['postText'].map(race)
data['race']=data.apply(raceapply2,axis=1)
data=data.groupby('postTitle').apply(get_head).reset_index(drop=True)
#data.drop_duplicates(data['postTitle'],inplace=True)
print data.shape
#print data['postText']
#print data['postTitle']
#print data.keys()
def vectorize(x=None):
    TF=TfidfVectorizer(ngram_range=(2,2))
    TF.fit(data['postTitle'])
    pickle.dump(TF,open('TF.pkl','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    return
def truncate(x=None):
    TF=pickle.load(open('TF.pkl','rb'))
    TSVD=TruncatedSVD(n_components=60)
    TSVD.fit(TF.transform(data['postTitle']))
    pickle.dump(TSVD,open("TSVD.pkl",'wb'),protocol=pickle.HIGHEST_PROTOCOL)
    return
def clusterize(x=None):
    '''Allows easy identification of certain posting styles'''
    TF = pickle.load(open('TF.pkl','rb'))
    TSVD=pickle.load(open("TSVD.pkl",'rb'))
    KM=MiniBatchKMeans(n_clusters=120)
    print "fitting vectorizer"
    data['cluster']=KM.fit_predict(TSVD.fit_transform((TF.fit_transform(data['postTitle']))))
    print data['cluster'].value_counts()
    for i in set(data['cluster']):
        print "cluster"+str(i)
        for j in data['postTitle'][data['cluster']==i].head(10):
            print j
    print data.groupby(['cluster','City'])['cluster'].count()
    return
#vectorize()
#truncate()
clusterize()
