#!/bin/sh
  

mkdir data
# Download the training and the test corpus
wget -nv --show-progress -O data/test.csv.zip https://www.dropbox.com/s/xp6bo8yo1vbv5yg/test.csv.zip?dl=1
wget -nv --show-progress -O data/train.csv.zip https://www.dropbox.com/s/xei6z41mfrcnxcd/train.csv.zip?dl=1
# Download the pretrained weights for bert base.
wget -nv --show-progress -O data/uncased_L-12_H-768_A-12.zip \
        https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip
wget -nv --show-progress  -O data/cased_L-12_H-768_A-12.zip \
        https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip
# unzip weights & conifg and remove the original zip
unzip -d data/ data/cased_L-12_H-768_A-12.zip && rm data/cased_L-12_H-768_A-12.zip
unzip -d data/ data/uncased_L-12_H-768_A-12.zip && rm data/uncased_L-12_H-768_A-12.zip
