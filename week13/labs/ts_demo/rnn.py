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

# Split the data into our target and actuals
yact = batch[:, :5]
x = batch[:, 5:]


# Create a mask so we can tell the model where our padding is
mask = x == -1
pd.DataFrame(x[:,:,0].numpy().transpose())

# First lets normalise our data
dmean = x[~mask].mean()
dstd = x[~mask].std()

x[~mask] = (x[~mask] - dmean) / dstd

xdf = x.squeeze(-1).numpy().transpose()
pd.DataFrame(xdf[::-1]).plot()
ydf = yact.squeeze(-1).numpy().transpose()
pd.DataFrame(ydf[::-1]).plot()



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

model = TimeSeriesRNN(input_feats = 1, outlen = yact.size(1), hidden = 32)
model

ypred = model(batch)
loss = criterion(ypred, yact)
loss

# Lets add categories to our data
PADCATSVALUE = 0
xcats = torch.randint(1,5, (x.shape))
xcats[mask] = PADCATSVALUE
pd.DataFrame(xcats.squeeze(-1).numpy().transpose())

xinp = torch.cat((x, xcats), -1)

xinp.shape

class TimeSeriesRNN(nn.Module):
    def __init__(self, input_conts, outlen, hidden_dim = 32):
        super().__init__()
        self.rnn = nn.LSTM(input_size=input_conts+hidden_dim,
                           hidden_size=hidden_dim,
                           batch_first=True, 
                           bidirectional = False)
        self.fc = nn.Linear(in_features=hidden_dim ,out_features=1)
        self.bn = nn.BatchNorm1d(num_features=1)
        self.embed = nn.Embedding(5, hidden_dim)
        self.outlen = outlen
        self.contidx = 0
        self.catidx = 1

    def forward(self, xinp):

        xcont = xinp [:,:, [self.contidx]] .permute(0 ,2, 1)
        xcont =  self.bn(xcont)
        xcont = xcont.permute(0 ,2, 1)
        
        xcat = xinp[:,:, self.catidx].long()
        xemb = self.embed(xcat)
        
        x = torch.cat((xcont, xemb), -1)
        
        hidden, _ = self.rnn(x)
        hidden = hidden[:,:self.outlen]
        
        out = self.fc(hidden)
        
        return out

self = model = TimeSeriesRNN( 1, yact.size(1),  32)
ypred = model(xinp)
loss = criterion(ypred, yact)
loss



# Transformers
mha = torch.nn.MultiheadAttention(embed_dim = 32, num_heads = 4)
embed = nn.Embedding(5, hidden_dim)
fc = nn.Linear(in_features=hidden_dim ,out_features=1)

xcats = xinp[:, :, 1].long()
xemb = embed(xcats)
# https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
'''
Shapes for inputs:
query: (L, N, E)(L,N,E) where L is the target sequence length, N is the batch size, E is the embedding dimension.
key: (S, N, E)(S,N,E) , where S is the source sequence length, N is the batch size, E is the embedding dimension.
value: (S, N, E)(S,N,E) where S is the source sequence length, N is the batch size, E is the embedding dimension.
'''
xemb.shape
xemb = xemb.permute(1, 0, 2)

attn_output, attn_output_weights = mha(xemb[:5], xemb, xemb)

'''
Shapes for outputs:
attn_output: (L, N, E)(L,N,E) where L is the target sequence length, N is the batch size, E is the embedding dimension.
attn_output_weights: (N, L, S)(N,L,S) where N is the batch size, L is the target sequence length, S is the source sequence length.
'''
attn_output.shape
attn_output = attn_output.permute(1,0,2)
ypred = fc(attn_output)
loss = criterion(ypred, yact)
loss

