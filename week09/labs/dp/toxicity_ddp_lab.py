import sys, os
import numpy as np 
import pandas as pd 
import torch
import torch.nn as nn
import torch.utils.data
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score
import pickle
import shutil

import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist
from torch.cuda.amp import autocast

from tqdm import tqdm,trange

from transformers import BertModel, BertConfig, BertTokenizer, BertForSequenceClassification, BertTokenizerFast
from transformers import AdamW as BertAdam
import logging

logger = logging.getLogger(__name__)


def load_data(data_dir, seed):
    DATA_DIR = data_dir + '/'
    train_size= 200000 # 1000000 
    valid_size= 100000  # 500000
    MAX_SEQUENCE_LENGTH = 220
    
    train_all = pd.read_csv(os.path.join(DATA_DIR, "train.csv.zip")).sample(train_size+valid_size,random_state=seed)
    print('loaded %d records' % len(train_all))
    # Make sure all comment_text values are strings
    train_all['comment_text'] = train_all['comment_text'].astype(str) 
    
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased',do_lower_case=True)
    logger.info("tokenizing..")
    sequences = tokenizer(train_all["comment_text"].fillna("DUMMY_VALUE").tolist(), truncation=True, add_special_tokens=True, padding=True, max_length = MAX_SEQUENCE_LENGTH)
    train_all=train_all.fillna(0)
    sequences = sequences.input_ids
    
    train_all['target']=(train_all['target']>=0.5).astype(float)
    # Training data - sentences
    X = sequences[:train_size] 
    # Target - the toxicity. 
    y = train_all[['target']].values[:train_size]
    X_val = sequences[train_size:]                
    y_val = train_all[['target']].values[train_size:]
    
#    test_df=train_all.tail(valid_size).copy()
#    train_df=train_all.head(train_size)

    train_dataset = torch.utils.data.TensorDataset(torch.tensor(X,dtype=torch.long),torch.tensor(y,dtype=torch.float))
    val_dataset = torch.utils.data.TensorDataset(torch.tensor(X_val,dtype=torch.long),torch.tensor(y_val,dtype=torch.float))
    
    return train_dataset,val_dataset

def dist_train(rank, world_size, data_dir, epochs):

    logger.info("Running on rank: %i", rank)
    seed=1234
    lr=2e-5
    batch_size = 32
    accumulation_steps=1
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    
    torch.cuda.set_device(rank)
    
    
    
    logger.info('loading data..')
    train_dataset, val_dataset = load_data(data_dir, seed)
    y_columns=['target']
    
    # use torch.utils.data.distributed.DistributedSampler here to create a sampler.
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=batch_size,
                                               shuffle=False,
                                               num_workers=0,
                                               pin_memory=True,
# uncomment this once you have your sampler working
#                                               sampler=train_sampler
                                              )
    logger.info("len of train_loader: %i", len(train_loader))
    
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=len(y_columns)).cuda()
    # move model to GPU with id rank
    # use nn.parallel.DistributedDataParallel to put your model on multiple GPUs
    # replace the line below with your own
    ddp_model = model

    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    
    optimizer = BertAdam(optimizer_grouped_parameters, lr=lr)
    
    tq = trange(epochs)
    for epoch in tq:
        ddp_model.train()
        ddp_train(rank, world_size, ddp_model, train_loader, optimizer, accumulation_steps)
        
    if rank == 0:
        torch.save(ddp_model.state_dict(), CHECKPOINT_PATH)


def ddp_train(rank, world_size, model, train_loader, optimizer, accumulation_steps):

        avg_loss = 0.
        avg_accuracy = 0.
        lossf=None
    
        scaler = torch.cuda.amp.GradScaler()
        device = torch.cuda.current_device()
        print("current device is: ", device)
    
        tk0 = tqdm(enumerate(train_loader),total=len(train_loader),leave=False)
        optimizer.zero_grad()  
        for i,(x_batch, y_batch) in tk0:
#        for i,(x_batch, y_batch) in enumerate(train_loader):
            with autocast():
                y_pred = model(
                    x_batch.to(device), 
                    attention_mask=(x_batch>0).to(device), 
                    labels=None)[0]
                loss =  F.binary_cross_entropy_with_logits(y_pred,y_batch.to(device))
                
            scaler.scale(loss).backward()
            if (i+1) % accumulation_steps == 0:             
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
            
            if lossf:
                lossf = 0.98*lossf+0.02*loss.item()
            else:
                lossf = loss.item()

            tk0.set_postfix(loss = lossf)
            avg_loss += loss.item() / len(train_loader)
            avg_accuracy += torch.mean(((torch.sigmoid(y_pred[:,0])>0.5) == (y_batch[:,0]>0.5).to(device)).to(torch.float) ).item()/len(train_loader)


def main():
    DATA_DIR = './data'
    EPOCHS = 2

    # these come from MPI
    if 'OMPI_COMM_WORLD_RANK' in os.environ:
      rank = int(os.environ['OMPI_COMM_WORLD_RANK'])
    else:
      rank = 0
    if 'OMPI_COMM_WORLD_SIZE' in os.environ:
      world_size = int(os.environ['OMPI_COMM_WORLD_SIZE'])
    else:
      world_size = 1

    # these are needed for pytorch distributed
    os.environ['WORLD_SIZE'] = str(world_size)
    os.environ['RANK'] = str(rank)
    # we only have one node, so...
#     os.environ['LOCAL_RANK'] = rank
   
    if 'MASTER_ADDR' not in os.environ:
      os.environ['MASTER_ADDR'] = 'localhost'
    
    if 'MASTER_PORT' not in os.environ:
      os.environ['MASTER_PORT'] = '12345'

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO if rank in [-1, 0] else logging.WARN,
    )
    world_size = int(world_size)
    logger.info("starting rank: %i, world size: %i", rank, world_size)         

#    dist.init_process_group(backend='nccl', init_method='env://', world_size=world_size, rank=rank)
    torch.distributed.init_process_group(backend="nccl")

    logger.info("all done")
    dist_train(rank, world_size, DATA_DIR, EPOCHS)

    dist.destroy_process_group()
    logger.info("all done")


if __name__ == "__main__":
    main()
