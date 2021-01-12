## AWS GPU VMs and Nvidia GPU Cloud (NGC)

In this lab, we will learn about our options when provisioning GPU instances in EC2. 

### AWS - nanolab part 1
1. Browse the current list of [ec2 instance types](https://aws.amazon.com/ec2/instance-types/).  What are the GPU options?
2. What are the current prices ($/hr) ? What are the most cost effective ones (trick question alert, we will be covering this in subsequent classes in more detail!)

### AWS - nanolab part 2
1. Let's provision an instance type as per the class discussion. Let's use our key as previously created and Nvidia Deep Learning AMI from AWS marketplace.  
In section 4, Storage, make sure that the root fs is increased to 100 GB.
2. Once provisioned, ssh to the instance.  
3. Ensure that docker works (e.g. `docker ps` does not fail)
4. Ensure that we can see our GPU(s) - e.g. `nvidia-smi` works

### Nvidia GPU Cloud - nanolab part 3
1. Examine categories at the [NGC homepage](http://ngc.nvidia.com). 
2. Under "containers", find the latest pytorch container. docker pull it
3. Can you launch this container on your GPU AWS instance and make sure that it sees the GPU inside it (hint: make sure you pass the gpu to your container)
4. (Extra credit) Can you modify the docker configuration so that the GPU is passed in by default?
5. Can you find jetson containers? What are they?

### AWS - nanolab part 4
1. Let's remove the VM that we provisioned in part 2
2. Provision an instance with the same GPU but use Ubuntu 20.04 as the OS
3. Using instructions [here](https://github.com/NVIDIA/nvidia-docker) install all of the pre-requisites (the driver, docker, and eventually, nvidia-docker)
4. The end result should be identical to [2] - e.g. `docker ps` should work. Note that while a bit complex, these steps are the "official" way to configure your machine
for GPU use


### Docker hub - nanolab part 5
1. Examine the [Docker hub](http://hub.docker.com) page
2. Find the latest ubuntu container. How big is it?
3. Pull it into your VM.. How can you tell how big the image is?
4. Find and pull the alpine image. How big is it?
5. (Extra credit) Can you find the Kaggle docker image? How big is it?
5. Please remove your VM(s) once you are done
