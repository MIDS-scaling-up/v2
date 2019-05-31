# Homework 6: The TPUs (and BERT!) IS BEING REVISED AND WILL BE RELEASED SHORTLY.  SUMMER 2019 STUDENTS PLEASE HOLD OFF STARTING IT

1. Read the Google Cloud Product Overview on the [TPUs](https://cloud.google.com/tpu/)  
2. Read the primer on [Bert](https://github.com/google-research/bert)  
3. Follow the below steps to run BERT in pytorch on the Jigsaw Toxicity classification dataset.  
  
Instructions on your assignment and training BERT in the book.   
* The book is set with 10K rows training and 5K rows validation - so you can test it fast in your initial development. For your final run, we would like you to train on at least 1M rows; and validate on at least 500K rows.  
* Please run it on a V100 VM and a P100 VM and report run times on training 1M rows on both. (Note, V100 will be faster, so maybe good to start there).   
* You have 8 sections found in the jupyter notebook to complete the training of BERT and answer some questions. The first 5 seem challenging - but there is a script linked in the book which should make it trivial - should be just copy and pasting from and to the correct places.   
* Your submission should be your completed notebook (either from the P100 or V100). You can submit either through a HTML or link to a private GitHub repo.   
* Please let your instructors know if it is taking an excessive amount of time. The scripts do run long on 1M rows ~ a number of hours on the both types of VM's, but the development should not take an excessivement amount of time.  
* The final section in the book shows a number of tasks, you need only complete 1 of them.   
  
  
## Images are in work - and will be updated here, but you can get started by creating your own VM's if you wish to start early.  
   
   
Start your `ibmcloud` VM. I ran like below - note this is a P100. For a V100, you need flavor `AC2_8X60X100`.  
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100 --domain=darragh.com --os=UBUNTU_16_64 --flavor AC1_8X60X100 --billing=hourly --san --disk=100 --disk=2000 --network 1000  --key=1418191
```

`ssh` into your machine and run the below. 
```
# Install cuda - referenced from - https://github.com/dimsav/grin-guide/wiki/Install-nvidia-driver-(cuda)
apt-get update
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
dpkg -i cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
apt-get update
apt-get install cuda
# Add to your bashrc file
echo 'export PATH="/usr/local/cuda/bin:$PATH"' >> ~/.bashrc
```
  
As per week 02, install docker.
```
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# add the docker repo    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# install it
apt-get update
apt-get install docker-ce

curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update

apt-get install -y nvidia-docker2
pkill -SIGHUP dockerd
```
  
Test cuda is running in docker. 
```
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
```

Now download your assignment. 
```
git clone https://github.com/MIDS-scaling-up/v2
```

Go into the directory for week 06 and download the datasets with this helper script.  
Note that we are downloading the pertrained BERT model published by google. During following steps we will be converting this to PyTorch.  
Please check your files in the `download.sh` script downloaded and unzipped correctly.   
```
cd v2/week06/hw/data/
sh download.sh
```

Let's grab our image and run it. You do not need the commented steps, but just so you are aware how it is built. 
```
# docker login
# docker build -t torchimg -f v2/week06/hw/PYTORCH.build .
# docker tag 386b7d7e5d24  w251/pytorch_gpu_hw06:latest # you can see your tag with command `docker images`
# docker push w251/pytorch_gpu_hw06

# Just run the below
cd ~
docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/pytorch_gpu_hw06
```
  
After you run this you will get an output like below. Go into your book, replacing the public IP in the brackets. For example for the below you can go to url   `http://158.176.131.11:8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e`
```
	root@p100:~# docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/pytorch_gpu_hw06
	[I 18:46:45.371 NotebookApp] Serving notebooks from local directory: /workspace
	[I 18:46:45.371 NotebookApp] The Jupyter Notebook is running at:
	[I 18:46:45.371 NotebookApp] http://(bef46d014d15 or 127.0.0.1):8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e
	[I 18:46:45.371 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

```

If you kill the above terminal, your notebook will stop. If you would like to keep your notebook permanently open you can run the docker in the background with `screen`, like below : 
```
# Enter `screen`
screen
docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/pytorch_gpu_hw06 
# to exit screen, type ctrl+d on your keyboard, and the command will keep running. To enter it again, type ctrl+a
```



