# Lab: LSTM Language model with OpenSeq2Seq

## Overview OpenSeq2Seq

OpenSeq2Seq is a TensorFlow-based toolkit for training sequence-to-sequence models:

* machine translation (GNMT, Transformer, ConvS2S, …)
* speech recognition (DeepSpeech2, Wave2Letter, Jasper, …)
* speech synthesis (Tacotron2, …)
* language model (LSTM, …)
* sentiment analysis (SST, IMDB, …)

## Main features:
modular architecture that allows assembling of new models from available components
support for mixed-precision training, that utilizes Tensor Cores introduced in NVIDIA Volta GPUs
fast, simple-to-use, Horovod-based distributed training and data parallelism, supporting both multi-GPU and multi-node


## Setup: get a GPU VM in Softlayer
Follow instructions in [Homework 9](https://github.com/MIDS-scaling-up/v2/tree/master/week09/hw) to get a T4 GPU VM in AWS, e.g.:
```
aws ec2 run-instances --image-id ami-0dc2264cd927ca9eb --instance-type g4dn.2xlarge --security-group-ids your_security_group --associate-public-ip-address --key-name yourkey_group
```

Pull and launch the latest Nvidia TF container, e.g.

```
# replace /data in the command with the location of your large data files so you don't need to copy them into your container
nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v /data:/data -it --rm nvcr.io/nvidia/tensorflow:19.03-py3
```

## Training an OpenSeq2Seq-based language model
We will generally follow [OpenSeq2Seq LM training intructions](https://nvidia.github.io/OpenSeq2Seq/html/language-model.html), please refer to them as needed.

A. __Data download:__
We will discuss the best option to move the data from the LazyNLP / GPFS cluster into IBM Cloud, please refer to the discussed Cloud storage options (async video) and try to come up with ideas about it.

B. __Edit your config file:__
```
cd example_configs/lm
Edit the file lstm-wkt2-fp32.py and set the data_root variable, e.g.
# data_root = "/data/wikitext-2"
# also make sure that horovod is turned off and that you're training on just 1 GPU (see the corresponding variables)

Make a copy of the downoaded data files to fit the expected format, i.e.(your path might look different)
cp /data/wikitext-2/wiki.train.tokens /data/wikitext-2/train.txt
cp /data/wikitext-2/wiki.valid.tokens /data/wikitext-2/valid.txt
cp /data/wikitext-2/wiki.test.tokens /data/wikitext-2/test.txt
```
C. __Kick off training:__
```
python run.py --config_file=example_configs/lm/lstm-wkt2-fp32.py --mode=train_eval --enable_logs
```
D. __Transfer the lazynlp data from your GPFS cluster to your VM__
* How do you transfer Gutenberg, Reddit files over?
* How do you kick off training?

F. __Exploration (optional):__
Review the [LM training docs](https://nvidia.github.io/OpenSeq2Seq/html/language-model.html) and try different combinations of settings and hyperparameters for training, share your experiences with the class 
