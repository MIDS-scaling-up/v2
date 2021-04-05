import pandas as pd
import numpy as np
import torch
from torch import nn
# Load the sequence data
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
confdf = pd.read_csv( f'{url}/time_series_covid19_confirmed_global.csv' )

confdf.iloc[0]

confdf = confdf.drop(['Province/State',  'Lat', 'Long'], 1).set_index('Country/Region')
confdf

confdf.loc['Afghanistan'].plot()
confdf.loc['Italy'].plot()

'''
Normalisation
'''
# Lets look at the distribution of our data
pd.Series(confdf.values.flatten()).hist(bins = 100)

pd.Series(np.log(1+ confdf.values.flatten())).hist(bins = 100)

pd.Series(np.log(1+ confdf.values.flatten()) /20 ).hist(bins = 100)

# so lets log norm it and divide by 20
def normfn(m):
    return np.log(1+m) / 20
def revnormfn(m):
        return np.exp(20 * m) - 1

confdf.values
normfn(confdf.values)
revnormfn(normfn(confdf.values))

'''
Transform data
'''
data = torch.tensor(normfn(confdf.values)).float() 
data.shape
data = data.unsqueeze(2)
data.shape
data = data.permute(0,2,1)
data.shape

trndata = data[:,:,:-5]
tstdata = data[:,:,-5:]


'''
Prototype Modelling
'''

x = data[:4]
x.shape
# Lets create a class to store our model. 
bn0 = nn.BatchNorm1d(num_features=1)

x = bn0(x)
x.shape

x = x.permute(0,2,1)
x.shape

hidden = 32
rnn = nn.LSTM(1, hidden)

rnn(x)



class TimeSeriesRNN(nn.Module):
    def __init__(self, hidden = 32):
        super().__init__()
        self.rnn = nn.LSTM(IN_UNITS, 32)
        self.n_features = self.cnn.fc.in_features
        self.cnn.global_pool = nn.Identity()
        self.cnn.fc = nn.Identity()

    def forward(self, x):
        bs = x.size(0)
        features = self.cnn(x)
        features = features.permute(0, 2, 3, 1)
        return features



