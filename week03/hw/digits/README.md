# Homework 3: Digits in a separate VM in Softlayer
We can use GPUS to train neural networks, but the Jetson's GPU is too weak for regular jobs. We'll instead use IBM's SoftLayer service in the cloud to provision a VS with Tesla P100s. Then we'll set up DIGITS on the VS and train the GoogLeNet neural network on the ImageNet dataset. This homework is not very complicated, but the steps do take some time.  Also, we use a P-100 VM in SoftLayer, which currently costs a lot (about $4 / hr)  so we suggest you start on this homework 48 hours before the class and collapse it after the instructors got a chance to review your work.

### Provision the VM 
We are using two P-100 GPUs for this VM, the fastest currently available in SoftLayer that we tested (Note that the faster V-100s have just been released there as well).  We are using Ubuntu 16 as the OS as of right now, since SL does not yet support 18.04 with GPUs.

Notice that we are getting two disks; the larger one will be used for dataset storage later on.
```
# replace the things in <> with your own values
ibmcloud sl vs create --datacenter=dal13 --hostname=<hostname> --domain=<domain> --os=UBUNTU_16_64 --flavor AC1_16X120X25 --billing=hourly --san --disk=25 --disk=2000 --network 1000 --key=<your SL key>

# for instance, this is what I did:
ibmcloud sl vs create --datacenter=dal13 --hostname=p100 --domain=dima.com --os=UBUNTU_16_64 --flavor AC1_16X120X25 --billing=hourly --san --disk=25 --disk=2000 --network 1000 --key=p305
``` 
### Install cuda
As of right now, 10.1 is the latest version.  Check https://developer.nvidia.com/cuda-toolkit  for the latest.
```
wget https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda-repo-ubuntu1604-10-1-local-10.1.168-418.67_1.0-1_amd64.deb
dpkg -i cuda-repo-ubuntu1604-10-1-local-10.1.168-418.67_1.0-1_amd64.deb


# the cuda 10.1 key
apt-key add /var/cuda-repo-10-1-local-10.1.168-418.67/7fa2af80.pub

# install it!
apt update
apt install -y cuda
```
If you have a dependency on cuda 10.0 (e.g. DeepStreamSDK), you will have to install these instead:
```
wget https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda-repo-ubuntu1604-10-0-local-10.0.130-410.48_1.0-1_amd64
dpkg -i cuda-repo-ubuntu1604-10-0-local-10.0.130-410.48_1.0-1_amd64 . 

# the cuda 10.0 key
apt-key add /var/cuda-repo-10-0-local-10.0.130-410.48/7fa2af80.pub

# install it!
apt-get update
apt-get install -y cuda
```

### Install docker
Validate these at https://docs.docker.com/install/linux/docker-ce/ubuntu/
```
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
	
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"	

apt-get update


# Dima validated on 01/13/19 that this below is still required; sigh
# apt-get install docker-ce=5:18.09.0~3-0~ubuntu-xenial
# As of 2/24/19 this works now
apt-get install -y docker-ce

# verify

docker run hello-world
```

### Install nvidia-docker (version 2)
First, add the package repositories
```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
```

Now, install nvidia-docker2 and reload the Docker daemon configuration
```
apt-get install -y nvidia-docker2
pkill -SIGHUP dockerd
```
Test nvidia-smi with the latest official CUDA image
```
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
```
Hopefully, you will see your GPUs.  
### Prepare the second disk
What is it called?
```
fdisk -l
```
You should see your large disk, something like this
```
Disk /dev/xvdc: 2 TiB, 2147483648000 bytes, 4194304000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```
In this case, our disk is called /dev/xvdc.  Your disk may be named differently.  Format it:
```
# first
mkdir -m 777 /data
mkfs.ext4 /dev/xvdc
```

Add to /etc/fstab
```
# edit /etc/fstab and all this line:
/dev/xvdc /data                   ext4    defaults,noatime        0 0
```
Mount the disk
```
mount /data
```
### Move the working Docker directory
By default, docker stores its images under /var/lib/docker , which will quickly fill up.  So,
```
service docker stop
cd /var/lib
cp -r docker /data
rm -fr docker
ln -s /data/docker ./docker
service docker start
```

### Start Digits in a container
Login into nvcr.io
```
# make sure you register at https://ngc.nvidia.com and enter your credentials when prompted
docker login nvcr.io
```
Pull and start the container.  Note that we are using 18.10 here; you will likely need to pull the latest.  Note also that we are passing through the /data disk to the container to be used for datasets:
```
# check the latest version of the Digits container here: https://ngc.nvidia.com/catalog/containers/nvidia%2Fdigits
# at this moment, the object detection example is broken in the latest digits container, so use the older one.
# nvidia-docker run --shm-size=1g --ulimit memlock=-1 --name digits -d -p 8888:5000 -v /data:/data -v /data/digits-jobs:/workspace/jobs nvcr.io/nvidia/digits:18.10
# a
nvidia-docker run --shm-size=1g --ulimit memlock=-1 --name digits1 -d -p 8888:5000 -v /data:/data -v /data/digits-jobs:/workspace/jobs nvidia/digits
```
### Validate that Digits is running
DIGITS is now running on your VS! To access it, make note of the public IP address of your VS and connect to it in a web browser window by typing the following into the address bar (replace <> with your VS IP address): `<ip-address>:8888`

You can exit and start the DIGITS container again at any time. 

## Training a Model on DIGITS
With DIGITS and our VS set up, we can now create a dataset and train a model with DIGITS. **Creating the dataset and training the model will take a substantial amount of time! Although you don't have to monitor the computer during these processes, the total time needed to reach the end may take over a day.**

The dataset we'll use is the ImageNet1000, which contains images classfied in 1000 categories such as "dog" or "car" with over 1 million images total. Larger datasets mean more examples for a model to train itself on.

The model we'll use is GoogLeNet, a convolutional neural network created by Google. Trained on the ImageNet dataset, it won the 2014 Imagenet competition. 

### Creating the Dataset
First, make sure DIGITS is running on your VS and open on a browser window. Find the "Datasets" tab and select it. Select the small blue button under the words "New Dataset" labeled "Images" and choose "Classification" in the drop-down menu. Now in the New Image Classification Dataset window, find the section for "Training Images". Paste this URL, where we have the entire Imagenet stored on a server:
```
http://169.44.201.108:7002/imagenet/train/
```
All other options can remain their default (for now). Give this dataset an appropriate Group and Dataset name, then select "Create". This process will take some time! 

### Training the Model
Return to the DIGITS home screen and select the "Models" tab. Once again, select "Classification" from the "Images" drop-down. In the 'Select Dataset' section, click on the dataset you previously created. Change the "Training epochs" value to 60 and set the "Batch size" value to 128. In the "Blob format" drop-down menu, select "Compatible". This slows the process somewhat but ensures the model is compatible with older versions of Caffe, such as on the Jetson for later. Underneath in the "Standard Networks" tab, select GoogLeNet. Select both Tesla P100 GPUs to use, give an appropriate Group and Model name, then click "Create". This process will take roughly 29 hours.

After training, observe the graphs. At which epochs do the accuracy rates (top graph) noticeably go up? How does the rate at which accuracy goes up change over epochs? At which epochs does the learning rate (botton graph) go down, and how much does it differ by each time? What were the final accuracy rates for Top 1 and Top 5? You can hover your mouse over lines for more details. You can also go to the "Trained Models" section to test images.

### Saving the Model
We'll save this trained model for future use on the Jetson (this is called transfer learning). Save the model *to your Jetson* by clicking the "Download Model" button. *This is very important!*

## Setting Up the Jetson for DIGITS

To prepare for future labs, we'll create a container with Caffe on the Jetson. Download the Dockerfile.caffebase and mutex.patch files and build the image:
```
docker build -t caffe -f Dockerfile.caffebase .
```
The DIGITS container that we will use in future labs will be based off of this Caffe container.
	
## Submission
Please submit screenshots of your trained GoogLeNet in Digits (the plot of loss vs epoch) along with the top 1 and top 5 final accuracy. Please submit the file name and size of the trained and downloaded model file. Also please submit the command line output of the docker build of the caffe container on the TX2
