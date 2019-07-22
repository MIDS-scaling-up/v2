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
Follow instructions in [Homework 6](https://github.com/MIDS-scaling-up/v2/tree/master/week06/hw) to get an image-based P100 VM in Softlayer, e.g.:
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=1418191 --flavor AC1_8X60X100 --san
```

Pull and launch the latest Nvidia TF container, e.g.

```
nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -it --rm nvcr.io/nvidia/tensorflow:19.06-py3
```

## Training an OpenSeq2Seq-based language model

A. __Data download:__
In this first iteration we will work the model with the dataset wikitext-2-v1, which is a small subset, feel free to expand the lab and share your experiences using the dataset that was collected with LazyNLP.
```
# update OpenSeq2Seq (optional since the TF container includes it anyways under /workspace/nvidia-examples/OpenSeq2Seq )
# git clone https://github.com/NVIDIA/OpenSeq2Seq
# cd OpenSeq2Seq
# pip install -r requirements.txt

# pull the wikitext dataset
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip
unzip wikitext-2-v1.zip
cd example_configs/lm
Edit the file lstm-wkt2-fp32.py and set the data_root variable, e.g.
# data_root = "/workspace/nvidia-examples/OpenSeq2Seq/wikitext-2"
Make a copy of the downoaded data files to fit the expected format, i.e.(your path might look different)
cp /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/wiki.train.tokens /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/train.txt
cp /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/wiki.valid.tokens /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/valid.txt
cp /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/wiki.test.tokens /workspace/nvidia-examples/OpenSeq2Seq/wikitext-2/test.txt
# kick off training:
python run.py --config_file=example_configs/lm/lstm-wkt2-fp32.py --mode=train_eval --enable_logs
```

C. __Exploration (optional):__
Review the official documentation and try different combinations of settings and hyperparameters, share your experiences with the class [OpenSeq2Seq](https://nvidia.github.io/OpenSeq2Seq/html/index.html)
