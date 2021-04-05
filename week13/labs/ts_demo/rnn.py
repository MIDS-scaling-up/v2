import pandas as pd
import numpy as np
import random
import torch
from torch import nn
random.seed(0)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

'''
Continuous Sequence data
'''
# Single sine wave sequence
def sinfn(f, slen, bias):
    return np.sin(np.linspace(-f, f, slen)) + bias

x  = sinfn(np.pi, 1000, 5)
pd.DataFrame(x).plot()

# Multiple sequences of different length
data = []
for i in range(8):
    f, slen, bias = random.uniform(2, 4), random.randint(100, 200), random.uniform(0, 5)
    x = torch.tensor(sinfn(f, slen, bias) + np.random.randn(slen)*0.1)
    x = x.unsqueeze(1).float()
    data.append(x)

# We have multiple lengths with one column in each sequence
[i.shape for i in data]

# Let's pad the sequences so they all get the same length
from torch.nn.utils.rnn import pad_sequence
PADVALUE = -1
batch = pad_sequence(data, batch_first = True, padding_value=PADVALUE)

batch.shape
batch[:,:1]
batch[:,-1:]


batchdf = batch.squeeze(-1).numpy().transpose()
pd.DataFrame(batchdf[::-1]).plot()


# Create a mask so we can tell the model where our padding is
mask = batch == -1
pd.DataFrame(mask[:,:,0].numpy().transpose())

# First lets normalise our data
dmean = batch[~mask].mean()
dstd = batch[~mask].std()

batch[~mask] = (batch[~mask] - dmean) / dstd

batchdf = batch.squeeze(-1).numpy().transpose()
pd.DataFrame(batchdf[::-1]).plot()

# Split the data into our target and actuals
yact = batch[:, :5]
x = batch[:, 5:]



# It's also good to apply batchnorm on the sequence data batches as the model trains. 
# https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html
bn0 = nn.BatchNorm1d(num_features=batch.size(-1))

bn0
x.shape
x.permute(0 ,2, 1).shape

x = bn0(x.permute(0 ,2, 1))
x.shape

x = x.permute(0 ,2, 1)


# Now let's try an RNN on the sequence data. 
#
hidden_dim = 32
# https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
lstm = nn.LSTM(input_size=1,hidden_size=hidden_dim,batch_first=True, bidirectional = False)
lstm
fc = nn.Linear(in_features=hidden_dim ,out_features=1)
fc

criterion = nn.MSELoss()


hidden, (h0, c0) = lstm(x)
hidden.shape, h0.shape, c0.shape

ypred = fc(hidden)
ypred.shape

# Let's get the loss
criterion = nn.MSELoss(reduction = 'none')
loss = criterion(ypred[:, :5], yact)
loss

criterion = nn.MSELoss()
loss = criterion(ypred[:, :5], yact)
loss


# Bring it all together 

class TimeSeriesRNN(nn.Module):
    def __init__(self, input_feats, outlen, hidden = 32):
        super().__init__()
        self.rnn = nn.LSTM(input_size=input_feats,
                           hidden_size=hidden_dim,
                           batch_first=True, 
                           bidirectional = False)
        self.fc = nn.Linear(in_features=hidden_dim ,out_features=1)
        self.bn = nn.BatchNorm1d(num_features=input_feats)
        self.outlen = outlen

    def forward(self, xinp):
        # xinp = batch
        x = xinp.permute(0 ,2, 1)
        x =  self.bn(x)
        x = x.permute(0 ,2, 1)
        
        hidden, _ = self.rnn(x)
        hidden = hidden[:,:self.outlen]
        
        out = self.fc(hidden)
        
        return out

# self = model = TimeSeriesRNN(input_feats = 1, outlen = yact.size(1), hidden = 32)
model = TimeSeriesRNN(input_feats = 1, outlen = yact.size(1), hidden = 32)
model

ypred = model(batch)
loss = criterion(ypred, yact)
loss
