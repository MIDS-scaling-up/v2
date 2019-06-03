# Customer Image creation  in Softlayer
With IBM® Cloud Virtual Servers image templates, you can capture a device's image to quickly replicate its configuration with minimal changes in the order process.

Image templates provide an imaging option for all Virtual Servers, regardless of operating system. Image templates allow you to capture an image of an existing virtual server and create a new one based on the captured image. 

When you request to create an image, the automated system of IBM Cloud™ takes your server offline. While the server is offline, a compressed backup of your data is created, the configuration information is recorded, and the image template is stored on the IBM Cloud SAN. During the deployment stage of the image template, the automated system constructs a new server that is based on the data that is gathered from the selected image. The deployment process makes adjustments for volume, restores the copied data, and then makes final configuration changes (for example, network configurations) for the new host.

### Provision the VM 
Provison a VSI with P-100 GPUs using Ubuntu 16 as the OS this will be the base virtual server for the image creation

```
# replace the things in <> with your own values
ibmcloud sl vs create --datacenter=dal13 --hostname=<hostname> --domain=<domain> --os=UBUNTU_16_64 --flavor AC1_16X120X25 --billing=hourly --san --disk=25 --disk=2000 --network 1000 --key=<your SL key>

# for instance, this is what I did:
ibmcloud sl vs create --datacenter=dal13 --hostname=p100 --domain=dima.com --os=UBUNTU_16_64 --flavor AC1_16X120X25 --billing=hourly --san --disk=25 --disk=2000 --network 1000 --key=p305
``` 
### Install cuda 10.0
**cuda 10.1 does not work too well with tensorflow and we will use this image for tensorflow in lab04**
```
apt-get update
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
dpkg -i cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
# the cuda 10.0 key
apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
# install it!
apt-get update
apt-get install cuda
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

	
## Image creation
Access the IBM® Cloud infrastructure [customer portal](https://control.softlayer.com/) by using your unique credentials.
1. From the Devices menu, select Device List.
2. Click the virtual server that you want to use to create an image template.
3. Check the Passwords tab of the Device Details page. Ensure that any passwords listed on the Device Details page match the actual operating system passwords and any other software add-on passwords. If passwords do not match, virtual servers that are created from this image template fail.
4. From the Actions menu, select Create Image Template.
5. Enter the new name for the image in the Image Name field.
6. Enter any necessary notes for the image in the Note field.
7. Select the Agree check box when all information is entered.
8. Click Create Template to create the image template.

## Ordering an instance from an image template
Access the IBM® Cloud infrastructure [customer portal](https://control.softlayer.com/) by using your unique credentials.
1. access the Image Templates page by selecting Devices > Manage > Images.
2. Click the Actions menu for the image template that you want to use and select the type of virtual server that you want to order.
3. On the Configure your Cloud Server page, complete all of the relevant information.
4. Click the Add to Order button to continue.
5. On the Checkout page, complete any advanced system configuration.
6. Click the Cloud Service terms and the Third-Party Service Agreement check boxes.
7. Confirm or enter your payment information and click Submit Order. You are redirected to a screen with your provisioning order number. You can print the screen because it's also your provisioning order receipt.

## Object Storage

Object storage is a modern storage technology concept and a logical progression from block and file storage. Object storage has been around since the late 1990s, but has gained market acceptance and success over the last 10 years.

Object storage was invented to overcome a number of issues:

*  Managing data at very large scales using conventional block and file systems was difficult because these technologies lead to data islands due to limitations on various levels of the data management hardware and software stack.

*  Managing namespace at scale resulted in maintaining large and complex hierarchies, which are required to access the data. Limitations in nested structures on traditional block and file storage arrays further contributed to data islands being formed.

*  Providing access security required a combination of technologies, complex security schemes, and significant human involvement in managing these areas.

Object storage, also known as object-based storage (OBS) uses a different approach to storing and referencing data. Object data storage concepts include the following three constructs:

*  Data: This is the user and application data that requires persistent storage. It can be text, binary formats, multimedia, or any other human- or machine-generated content.

*  Metadata: This is the data about the data. It includes some predefined attributes such as upload time and size. Object storage allows users to include custom metadata containing any information in key and value pairs. This information typically contains information that is pertinent to the user or application that is storing the data and can be amended at any time. A unique aspect to metadata handling in object storage systems is that metadata is stored with the object.

*  Key: A unique resource identifier is assigned to every object in an OBS system. This key allows the object storage system to differentiate objects from one another and is used to find the data without needing to know the exact physical drive, array, or site where the data is.

This approach allows object storage to store data in a simple, flat hierarchy, which alleviates the need for large,
performance-inhibiting metadata repositories.

Data access is achieved by using a REST interface over the HTTP protocol, which allows anywhere and anytime access simply by referencing the object key.

## Connect the VSI to Cloud Object storage

Ingredients
* Access to an IBM Cloud Object Storage (COS) bucket
* A Linux based system


The s3fs-fuse GitHub page has all the details on building and installing the package.
```
sudo apt-get update
sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
git clone https://github.com/s3fs-fuse/s3fs-fuse.git

```

Build and install the library
```
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install

```

In order to configure s3fs-fuse, you need your access key id, your secret access key, the name of the bucket you want to mount, and the endpoint for the 
If you are using the Infrastructure variation of Cloud Object Storage (i.e. softlayer), you can get these values from the ObjectStorage section in the Control Portal.

```
Substitue your values for <Access_Key_ID> and <Secret_Access_Key> in the below command.
echo "<Access_Key_ID>:<Secret_Access_Key>" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
```
Create a directory where you can mount your bucket. Typically, this is done in the /mnt directory on Linux, notice the bucket is created in the IBM Cloud UI
```
sudo mkdir /mnt/mybucket
sudo s3fs bucketname /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-east.objectstorage.softlayer.net

```
