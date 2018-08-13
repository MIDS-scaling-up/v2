# HW 2: Provisioning a VS in the Cloud with DIGITS
We can use GPUS to train neural networks, but the Jetson's GPU is too weak for regular jobs. We'll instead use IBM's SoftLayer service in the cloud to provision a VS with Tesla P100s. Then we'll set up DIGITS on the VS and train the GoogLeNet neural network on the ImageNet dataset.

## SoftLayer and the Cloud
Use your provided SoftLayer account credentials and log in at control.softlayer.com. Follow [these instructions](http://knowledgelayer.softlayer.com/procedure/generate-api-key) to generate an API key, used to log into SoftLayer's services via the shell. Treat this key as a private password, don't share it publicly, and make sure to remove and generate a new API key if your current key is compromised.

### Setting Up SoftLayer and slcli
We will use the SoftLayer CLI tool running in a Docker container to access the cloud. On the Jetson (or any computer with command line and Docker), create a new directory to store the slcli dockerfile. Download the Dockerfile.slcli file into this directory, open it, and then **change the username and API key values in the <> to your own.** Now build it:
```
docker build --tag slcli -f Dockerfile.slcli .
```
Now run the image in interactive mode:
```
docker run -it slcli
```
The resulting container has run slcli, so you can always restart it with `docker start -i <containerID>` to resume slcli.
Run the following command to set up slcli with your account. The default values provided for the questions are fine.
```
slcli config setup
```

### Working with SoftLayer VSes
slcli is used to work with SoftLayer VSes, though the SoftLayer website at control.softlayer.com can also be used. We'll usually work with low-RAM hourly virtual servers in this course. Use `slcli vs create` to provision a VS. Run the following to provision an example (make sure to replace hostname and domain with your own values):
```
slcli vs create --datacenter=dal09 --hostname=<somehostname> --domain=<some.domain> --os=CENTOS_7_64 --cpu=1 --memory=1024 --billing=hourly
```
Use `slcli vs create-options` to see VS provisioning options. Find the VS you just provisioned with: 
```
slcli vs list
```
When fully provisioned, your VS will show up listed like this:
```
:..........:..........:................:................:............:........:
:    id    : hostname :   primary_ip   :   backend_ip   : datacenter : action :
:..........:..........:................:................:............:........:
: 58253333 :<hostname>: 169.62.178.219 : 10.187.197.157 :   dal09    :   -    :
:..........:..........:................:................:............:........:
```
In order to use the VS you must access and log into it via ssh. First, use the following slcli command to check the VS's root password, replacing the <> with either the ID or primary IP address:
```
slcli vs credentials <ID/IP>
:..........:..............:
: username :   password   :
:..........:..............:
:   root   :<somepassword>:
:..........:..............:
```
Access the VS remotely via ssh (make sure to replace the <> with ID or IP), using the discovered password when prompted:
```
ssh root@<ID/IP>
```
Poke around for a bit, then exit the VS. Now deprovision the VS:
```
slcli vs cancel <ID/IP>
```

## DIGITS in the Cloud
We'll now provision a VS in the cloud with two Tesla P100s to run our DIGITS server. Provision it with the following command **(make sure to replace the <> with your own unique values)**:
```
slcli vs create --datacenter=dal13 --hostname=<hostname> --domain=<some.domain> --os=CENTOS_7_64 --flavor AC1_16X120X25 --billing=hourly --san --disk=25 --disk=2000 --network 1000
```
If you encounter an "insufficient capacity" error, change to a different data center that provides P100s.

### Setting up the VS for DIGITS
ssh into the VS with the previously learned commands, then run the following commands:
```
yum update -y
reboot
```
Re-enter the VS. Now install and test Docker with the following commands:
```
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce
systemctl start docker
docker run --rm hello-world
```
With Docker installed, set up CUDA:
```
wget https://developer.nvidia.com/compute/cuda/9.2/Prod2/local_installers/cuda-repo-rhel7-9-2-local-9.2.148-1.x86_64
rpm -Uvhi --nosignature cuda-repo-rhel7-9-2-local-9.2.148-1.x86_64
yum install -y epel-release
yum clean all
yum install -y cuda
yum install -y git pciutils
reboot
```
Re-enter the VS and then install and test Nvidia-Docker:
```
systemctl start docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo
sudo yum install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
```
Now prepare to mount the second disk:
```
mkdir -m 777 /data
mkfs.ext4 /dev/xvdc
```
Add the following line to the file at /etc/fstab (eg with vim text editor: open file in vim with `vim /etc/fstab`, type "i" to enter interactive mode, add the line, then hit "escape" to end interactive mode, type ":wq" to save and quit):
```
/dev/xvdc /data                   ext4    defaults,noatime        0 0
```
Mount the new disk:
```
mount /data
```

### Installing and Running DIGITS on the VS
In order to use the official DIGITS container by Nvidia, first create an account at ngc.nvidia.com. Sign into NGC, then go to the "Configuration" tab on the left and generate an API key. Going back to the VS, log into NGC with your API key:
```
docker login nvcr.io
```
You'll be prompted for credentials. The username is always "$oauthtoken" and enter your own API key. Finally, pull the DIGITS image from NGC and run it:
```
nvidia-docker run --shm-size=1g --ulimit memlock=-1 --name digits -d -p 8888:5000 -v /data:/data -v /data/digits-jobs:/workspace/jobs nvcr.io/nvidia/digits:18.06
```
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

We'll save this trained model for future use on the Jetson (this is called transfer learning). Save the model by clicking the "Download Model" button.

## Setting Up the Jetson for DIGITS

To prepare for the lab, we'll create a container with Caffe on the Jetson. Download the Dockerfile.caffebase and mutex.patch files and build the image:
```
docker build -t caffe -f Dockerfile.caffebase .
```
The DIGITS container in the week 2 lab will be based off of this Caffe container.
