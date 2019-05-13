### Docker 101
This lab is a primer on docker, which in the past few years emerged as the dominant workload management and deployment tool.

Docker - https://www.docker.com/  - is a collection of tools around Linux Containers [which are a lightweight form of virtualization]. 
Linux Containers have been part of the Linux kernel for quite some time now, but the user space tooling has lagged, which provided 
an opportunity for Docker as a company.  Recently, Docker became available on MacOS X and even on Windows 10 Professional or later, in addition
to Linux. Note that while Docker on MacOS X is "native", it requires an underlying hypervisor on Windows. It is important to realize
that a linux container shares the kernel with the underlying VM or host; there is no need to copy the entire OS.  This is why the containers
are very small and light, they are easy to spin up and you can have many of them on devices as small as Raspberry Pi Zero..

#### Installing docker
If you already have docker running, you may skip this step.  However, you may wish to do it if you never installed docker on ubuntu.
This assumes that you have an slcli installed somewhere, e.g. on a VM in softlayer or in your local environment.

Let us spin up a clean VM.  This will take a few minutes to come up:
```
 ibmcloud sl vs create --datacenter=dal09 --domain=<something here> --hostname=<something here> --os=UBUNTU_16_64 --cpu=1 --memory=1024 --billing=hourly --key=<your key>
```

#### ENSURE THAT YOU SECURE THE VSI'S SSH AGAINST ATTACKS USING THE INSTRUCTIONS IN HOMEWORK 2

Now, let us follow the official instructions here to install DockerCE on Ubuntu 16:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
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
```
#### Running and managing docker containers.
Let us validate that docker is installed:
```
docker run hello-world
```
If this completed successfully, you have successfully got your first docker container running!  Now. let's try to find it:
```
docker ps
```
This command should show you all active docker containers.  At this point, the list should be empty, since the hello-world container exited.  However, the container should still be there:
```
docker ps -a
# Should see something similar to the below:
# CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS                          PORTS               NAMES
# 94a841d96b07        hello-world         "/hello"            About a minute ago   Exited (0) About a minute ago                       elated_brahmagupta
```
Now, let us remove this docker container:
```
docker rm <container_id>
docker ps -a
```

The container should be gone now.

Let's get a ubuntu container going:
```
docker run --name my_ubuntu -ti ubuntu bash
# Your prompt should change to something like
# root@5cf4cef1b2ee:/#
```
This should have downloaded the docker ubuntu image,  created a container called my_ubuntu, started it, and attached a terminal to it.  At this point, you should be inside the container.  The -ti flag connects the current terminal to the container.  Do something inside this container, e.g. 
```
apt-get update
```
Now, let us temporarily disconnect from this container:
```
Ctrl-P Ctrl-Q
```
You should now be back in your VM.  Let's see what's running :
```
docker ps
# you should see your container is actively running.
# CONTAINER ID        IMAGE                              COMMAND              CREATED             STATUS              PORTS                               NAMES
# 30666624229d        ubuntu                             "bash"               17 seconds ago      Up 16 seconds                                           my_ubuntu

```
Now, let us reconnect to the container:
```
docker attach my_ubuntu
```
You should be now back inside the container.  You can play around with it; once you are done, just type
```
exit
```
This should return you from the container and also stop it.  Verify that it is no longer running:
```
docker ps
```
Now, let's start the container:
```
docker start my_ubuntu
docker ps
```
Now, let's re-attach to this container:
```
docker attach my_ubuntu
```
You are back in the container.  Once you are done, disconnect from it (Control-P Control Q), and then remove it as it is running:
```
docker rm -f my_ubuntu
```

#### Using Docker images
Docker containers are spawned from images.  Let's see what images we have locally on our machine:
```
docker images
# should see something like
# ubuntu                  latest               0ef2e08ed3fa        6 months ago        130MB
```
The images are located in docker repositories and are downloaded before the containers are started.  The main docker repository is the Docker Hub: https://hub.docker.com/  Take a moment to browse through the images, do a few searches:

Now, let us download the apache docker image: https://hub.docker.com/_/httpd/
```
docker pull httpd
```
Validate that the image is now available locally, e.g.
```
docker images
```
Now let us start apache.  Note that we are passing port 80 inside the container to port 8003 in our VM and also passing our current
directory to the /usr/local/apache2/htdocs inside the container.
```
docker run -d --name my-apache-app -p8003:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4
```
Now, let us edit index.html in our current directory and then point our browser to http://ip-of-my-vm  (you could get it from ifconfig)
You should be able to see that our http server is running!

#### Using Dockerfiles
We always want to automate deployment to the extent possible.  Let's see how we can create our own docker images.  Create a file called Dockerfile and write to it the following text:
```
# FROM nvidia/cuda
# FROM nvidia/cuda:8.0-cudnn6-devel
# FROM nvidia/cuda:8.0-cudnn5-devel
FROM ubuntu

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    python-pip \
    python-setuptools \
    python-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install h5py pandas
RUN pip install theano

RUN pip install --upgrade -I setuptools \
  && pip install --upgrade \
    keras

RUN pip install  \
    matplotlib \
    seaborn

RUN pip install scikit-learn tables
RUN pip install --upgrade pip
RUN pip install 'ipython<6'

RUN pip install jupyter

VOLUME /notebook
WORKDIR /notebook
EXPOSE 8888

ENV KERAS_BACKEND=theano

#  CMD jupyter notebook --no-browser --ip=0.0.0.0 --NotebookApp.token= --allow-root
CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root
```
Let's create an image from it:
```
docker build -t test .
```
This will take a minute or two and eventually create a new docker image.  List your docker images to ascertain that it was successfully created.

Now, let's start our test image:
```
docker run --name jupyter -p 8800:8888  -d test
```
In order to access the jupyter notebook, we need to get the access token.  It should be logged to docker stdout, so let's get it:
```
docker logs jupyter
#     Copy/paste this URL into your browser when you connect for the first time,
#   to login with a token:
#        http://0.0.0.0:8888/?token=378684ab93ca16a1348ba2cb874cb52dbc18362fe756648f
```
Now, point your browser to http://my_vm_ip:8800  and use the token to log in.

Once you are all done, remove the VM to avoid extra charges!

### Part 2 (Optional)

In this section, we’ll expand upon the private network concept we explored in HW2.
First, you’ll need to upload your private key to the jumpbox VM created in HW2.  
For example:

	```
    sftp root@<jumpboxVM>
    mput ~/.ssh/id_rsa
    ```

Then ssh back to the jump box move the key to the .ssh directory and update the permission:

```
	mv id_rsa ~/.ssh
    chmod 600 ~/.ssh/id_rsa
```

Next, create a VM with a private only network in the same datacenter has your jumpbox.  For example (ensuring to replace the key ID with your SSH Key ID):

```
ibmcloud sl vs create --hostname=test --private --domain=you.cloud --cpu=2 --memory=2048 --datacenter=ams03 --os=UBUNTU_16_64 --san --disk=100 --key=123456
```

Wait for the VM to be created, then SSH into it.  
Update the VM and install curl

	apt-get update
	apt-get install curl

Now try to connect to www.google.com

```
curl https://www.google.com
```

What happens?  Your connection should timeout.  This is because "private network only" systems do not have a connection to the internet.  We will now install an HTTP proxy on the jumpbox that will allow private network systems to reach the internet.  Exit out of the VM so that you are back on the jumpbox.

On the jumpbox, install docker (see the first part of the lab).  Once installed, copy squid.conf to the jumbox.  Then create the folder /root/proxy and move the squid.conf into it.
	
```
mkdir /root/proxy             
mv squid.conf /root/proxy/
```

We’ll need your VM’s private IP.  If you need to get it, you can run the command

```
ipconfig eth0
```

We’ll now start the proxy (for more details see https://github.com/sameersbn/docker-squid).

```
docker run --name squid -d --restart=always \
  --publish <privateIP>:3128:3128 \
  --volume /root/proxy/squid.conf:/etc/squid/squid.conf \
  sameersbn/squid:3.5.27-1

```
Login to your private VM.
Set the following environmental variables, replacing <jumpboxPrivateIP> with your jumpbox's private IP:

```
export http_proxy=http://<jumpboxPrivateIP>:3128
export https_proxy= http://<jumpboxPrivateIP>:3128
```

Now try to connect to www.google.com again

```	
curl https://www.google.com
```

And this time you should be able to connect.


### Bonus 
It is possible to install and use docker from your private network system.

Log into your "private network only" VM. Make sure you've exported the http_proxy and https_proxy eenvironmental variables, then install docker as you have done before.

Follow the instructions to install docker from part 1.

Once installed, you need to configure docker to use the HTTP proxy with the following steps (see https://docs.docker.com/config/daemon/systemd/#httphttps-proxy for additional details). 

Create a systemd drop-in directory for the docker service

```
mkdir -p /etc/systemd/system/docker.service.d
```

Create a file called /etc/systemd/system/docker.service.d/http-proxy.conf that adds the HTTP_PROXY environment variable:

```
[Service]
Environment="HTTP_PROXY=http://<jumpboxPrivateIP>:3128"
```

Create a file called /etc/systemd/system/docker.service.d/https-proxy.conf that adds the HTTPS_PROXY environment variable:

```
[Service]
Environment="HTTPS_PROXY=http://<jumpboxPrivateIP>:3128"
```

Making sure to replace <jumpboxPrivateIP> with the private IP address of your jumpbox.
Flush changes:

```
systemctl daemon-reload
```

And restart Docker:

```
systemctl restart docker
```

Now install the nginx image and have it listen on the host's port 80:

```
 docker run --name my-nginx -d -p 80:80 nginx
```

You may find additional details on proxy configuration for your docker containers at https://docs.docker.com/network/proxy/.

Now exit your private system and return to the jumpbox.

Validate that you can reach your nginx container:

```
curl http://<privateIPofVM>
```

And verify you get a response.  Logout of the jumpbox.

The following creates an SSH tunnel from your workstation to your private system via your jumpbox:

```
ssh -L 8080:<privateIPofVM>:80 root@<pubicIPofJumpbox>
```

From a local browser, open up http://localhost:8080 and you should see your containers welcome page.

Log out of your ssh session, pressing ctl+c to terminate tunneling.

### Delete all VMs except your jumpbox.




