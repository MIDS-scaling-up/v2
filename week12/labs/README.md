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


### Get a pair of GPU VMs in Softlayer
Follow instructions in [Homework 3](https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw) to get 1 P100 VM in Softlayer.  

Virtual servers middleware installation:

A. __Install GCC__
```
sudo apt-get update && sudo apt-get install build-essential software-properties-common -y && sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y && sudo apt-get update && sudo apt-get install gcc-snapshot -y && sudo apt-get update && sudo apt-get install gcc-6 g++-6 -y && sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 && sudo apt-get install gcc-4.8 g++-4.8 -y && sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8;
sudo update-alternatives --config gcc
```

B. __Install CUDA drivers:__

```
wget https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.105_418.39_linux.run
sh cuda_10.1.105_418.39_linux.run
Follow the prompts
```
C. __Install Docker CE:__
```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo docker run hello-world

```

C. __Install NVIDIA docker 2 and run the Tensorflow container:__
```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

sudo apt-get install nvidia-docker2
sudo pkill -SIGHUP dockerd

#Test it
docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
 
docker pull nvcr.io/nvidia/tensorflow:19.03-py3
 
 nvidia-docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -it --rm nvcr.io/nvidia/tensorflow:18.12-py3
```

## Tensorflow operations

A. __Data collection:__
In this first iteration we will work the model with the dataset wikitext-2-v1, which is a small subset, feel free to expand the lab and share your experiences using the dataset that was collected with LazyNLP.
```
git clone https://github.com/NVIDIA/OpenSeq2Seq
cd OpenSeq2Seq
pip install -r requirements.txt
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip
unzip wikitext-2-v1.zip
cd example_configs/lm
Edit the file lstm-wkt2-fp32.py and setup the appropiate path for the train, validation and test.
Make a copy of the data to fit the expected format, i.e.(your path might look different)
cp /workspace/OpenSeq2Seq/wikitext-2/wiki.train.tokens /workspace/OpenSeq2Seq/wikitext-2/train.txt
python run.py --config_file=example_configs/lm/lstm-wkt2-fp32.py --mode=train_eval --enable_logs
```

C. __Exploration (optional):__
Review the official documentation and try different combinations of settings and hyperparameters, share your experiences with the class [OpenSeq2Seq](https://nvidia.github.io/OpenSeq2Seq/html/index.html)
