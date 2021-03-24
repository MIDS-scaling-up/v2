# Homework: Part 1 - Installing GPFS FPO (THIS HOMEWORK IS BEEN UPDATED, PLEASE COME BACK 03/26/2021 TO FINISH THE SETUP)

## Overview

These instructions are a subset of the official instructions linked to from here: [IBM Spectrum Scale Resources - GPFS](https://www.ibm.com/support/knowledgecenter/en/STXKQY_5.0.1/com.ibm.spectrum.scale.v5r01.doc/bl1ins_manuallyinstallingonlinux_packages.htm).


We will install GPFS FPO with no replication (replication=1) and local write affinity.  This means that if you are on one of the nodes and are writing a file in GPFS, the file will end up on your local node unless your local node is out of space.

A. __Get three virtual servers provisioned__, 

Use this command to pick out your default vpc, note, it is the vpc with `"IsDefault": true`.
```
aws ec2 describe-vpcs | grep -B20 "IsDefault\": true" | grep VpcId
```

If you do not see a VpcId listed, try `aws ec2 describe-vpcs | grep VpcId`

My default VPC is `vpc-e4e35381`, I shall use this below. 

Now create a security group which will allow us to login. 
```
aws ec2 create-security-group --group-name hw12 --description "HW12" --vpc-id vpc-YOUR_VPC_ID
```

You should see output similar to this:
```
{
     "GroupId": "sg-0be9d9ccd3efee363"
}
```

Now allow ingress on port 22 and for ping:

```
aws ec2 authorize-security-group-ingress --group-id sg-YOUR_SG_ID  --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-YOUR_SG_ID --ip-permissions IpProtocol=icmp,FromPort=-1,ToPort=-1,IpRanges=[{CidrIp=0.0.0.0/0}]
aws ec2 authorize-security-group-ingress --group-id sg-YOUR_SG_ID  --protocol tcp --port 0-65535 --cidr 0.0.0.0/0
```
Now launch the ec2 instances with Centos 7 installed.
```
aws ec2 run-instances --image-id ami-0affd4508a5d2481b --instance-type t2.medium --security-group-ids sg-YOUR_SG_ID --associate-public-ip-address --block-device-mapping 'DeviceName=/dev/sda1,Ebs={VolumeSize=32}' --key-name YOUR_KEY_NAME --count 3
```

Create 3 EBS volumes of 100GB to attach to the ec2 instances as secondary drives by running the `create-volume` command **three times**:

```
aws ec2 create-volume --volume-type gp2 --size 100 --availability-zone us-east-1a
```
**NOTE: The availability zone can be found by running:**
`aws ec2 describe-instances | grep AvailabilityZone`


Attach 1 volume per ec2 instance, so each ec2 instance would end up having two volumes (boot and external 100 GB)
```
aws ec2 attach-volume --volume-id vol-YOUR_VOLUME_ID --instance-id i-YOUR_INSTANCE_ID --device /dev/sdf
```

**Notice that volume-id and instance-id would be different on each case.**


Now log in into the ec2 instances to finish the setup:
```
ssh -i "YOUR_KEY.pem" centos@YOUR_PUBLIC_DNS_NAME
```


B. __Set up each one of your nodes as follows:__

Switch to root user after you login:
```
sudo su -
```

Add to /root/.bash\_profile the following line in the end:

    export PATH=$PATH:/usr/lpp/mmfs/bin

Make sure the nodes can talk to each other without a password. Let's create ssh keys as centos user and distribute them across the nodes. Ensure that you accept the defaults (and do not set a passphrase):
```
[root@ip-172-31-70-9 ~]# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.

```
Add the new public key to the authorized_keys file:
```
# cat ~/.ssh/id_rsa.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOHcLvpsLtQrjPLn5CkwW6h1TAviRhCPI40y/j9/5GMYdG+F5yi65pWeWU5sM6BUKDUQK3mXdd0H7J2wLeUR7goIcpSxEV7CeJaQSdY3zc1J9yJjSBl+wABBnn16Csdp7D733wTM+fIkk9amJb0s+UKFQyUG/C centos@ip-YOUR_IP_ADDRESS.ec2.internal

```
Copy the contents of the above into the authorized_keys files on **each of the virtual servers**, for example:
```
vi ~/.ssh/authorized_keys 
append the values of:
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOHcLvpsLtQrjPLn5CkwW6h1TAviRhCPI40y/j9/5GMYdG+F5yi65pWeWU5sM6BUKDUQK3mXdd0H7J2wLeUR7goIcpSxEV7CeJaQSdY3zc1J9yJjSBl+wABBnn16Csdp7D733wTM+fIkk9amJb0s+UKFQyUG/C centos@YOUR_IP_ADDRESS.ec2.internal
```
**Do the same for all the 3 virtual servers so in the end you would have an authorized_keys file with 4 keys, 3 for the hw12 servers and your local key.**

Test that ssh connectivity between the hosts work. You should be able to ssh between any two nodes without a password. **THIS IS A KEY TEST**:
```
ssh IP_ADDRESS_OF_ANOTHER_SERVER
```
You can get the IP address for a server by running `ifconfig eth0 | grep inet | grep -v inet6 | awk '{print $2}'`

Modify the hosts file (/etc/hosts) for **each of the three nodes** in your cluster by adding all three the IP addresses and a name. For instance, your hosts file should look similar to this (but with different IP addresses):

    127.0.0.1 		localhost.localdomain localhost
    172.31.71.181  gpfs1
    172.31.74.163  gpfs2
    172.31.78.146  gpfs3
Try to connect with ssh from each host using the short name we added to the hosts file:
```
ssh root@gpfs1
ssh root@gpfs2
ssh root@gpfs3
```
All should connect without asking for password.

Create a nodefile on gpfs1.  Create /root/nodefile and add the names of your nodes.  This is a very simple example with just one quorum node:
```
gpfs1:quorum:
gpfs2::
gpfs3::
```

C. __Install and configure GPFS FPO on each node:__
Install pre-requisites on each node
```
#update the kernel & install some pre-reqs
yum install -y kernel-devel g++ gcc cpp kernel-headers gcc-c++ 
yum update
#reboot to use the latest kernel
reboot
#after reboot completes, log back in as root and install more pre-reqs
yum install -y ksh perl libaio m4 net-tools unzip

```
Then install S3 API client on `gpfs1` and download the GPFS install package (ensure that you use the shared Access Key and not your own credentials):

```
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
/usr/local/bin/aws configure
Access Key ID:
A1XGdUexhlIdyusn16Jh
Secret Access Key:
vImKKsEPfYQuzovEuPZjabeAViRhdQ9P85RQJEt1
/usr/local/bin/aws --endpoint-url=https://s3-api.us-geo.objectstorage.softlayer.net  s3 cp s3://homework12/Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install

# copy the file to the other nodes
scp Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install gpfs2:~
scp Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install gpfs3:~

```

GPFS installation (node that we are adding nodes using the node names, be sure to update the hosts file on each VM)
```
source /root/.bash_profile
chmod +x Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install
./Spectrum_Scale_Standard-5.0.5.0-x86_64-Linux-install --silent  #(this command needs to be run on every node)
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale node add gpfs1  #(this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale node add gpfs2  #(this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale node add gpfs3  #(this command needs to be run just gpfs1)

```


D. __Create the cluster.  Do these steps only on one node (gpfs1 in my example).__
```
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale setup -s IP-ADDRESS-OF-GPFS1  #(this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale callhome disable   #(this command needs to be run just gpfs1)
/usr/lpp/mmfs/5.0.5.0/installer/spectrumscale install  #(this command needs to be run just gpfs1)
```
Now the cluster is installed, let's work the details.

Now, you must accept the license:

     /usr/lpp/mmfs/bin/mmchlicense server -N all #(this command needs to be run just gpfs1)
    # (say yes)

Now, start GPFS:

    mmstartup -a #(this command needs to be run just gpfs1)

All nodes should be up ("GPFS state" column shows "active"):

    mmgetstate -a #(this command needs to be run just gpfs1)

Nodes may reflect "arbitrating" state briefly before "active".  If one or more nodes are down, you will need to go back and see what you might have missed. If some node shows a DOWN state, log into the node and run the command  mmstartup. The main GPFS log file is `/var/adm/ras/mmfs.log.latest`; look for errors there.

You could get more details on your cluster:

    mmlscluster #(this command needs to be run just gpfs1)

Now we need to define our disks. Do this to print the paths and sizes of disks on your machine:

    lsblk #(this command and the rest until the file creation command (touch aa) needs to be run just gpfs1)

Note the names of your 100G disk. Here's what I see:
```
[root@ip-172-31-65-131 ~]# lsblk
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
xvda    202:0    0   32G  0 disk 
└─xvda1 202:1    0   32G  0 part /
xvdf    202:80   0  100G  0 disk 
```

Note that the root file system `/` on the example above is `xvda1`

Identify the 100G disk on all three nodes.

Disk /dev/xvda (partition 1) is where my operating system is installed, so I'm going to leave it alone.  In my case, __xvdf__ is my 100G disk.  In your case, it could be /dev/xvdb, so __please be careful here__.  Assuming your 100G disk is `/dev/xvdf` then add these lines to `/root/diskfile.fpo`:

    %pool:
    pool=system
    allowWriteAffinity=yes
    writeAffinityDepth=1

    %nsd:
    device=/dev/xvdf
    servers=gpfs1
    usage=dataAndMetadata
    pool=system
    failureGroup=1

    %nsd:
    device=/dev/xvdf
    servers=gpfs2
    usage=dataAndMetadata
    pool=system
    failureGroup=2

    %nsd:
    device=/dev/xvdf
    servers=gpfs3
    usage=dataAndMetadata
    pool=system
    failureGroup=3

Now run:

    mmcrnsd -F /root/diskfile.fpo

You should see your disks now:

    mmlsnsd -m

Let’s create the file system.  We are using the replication factor 1 for the data:

    mmcrfs gpfsfpo -F /root/diskfile.fpo -A yes -Q no -r 1 -R 1

Let’s check that the file system is created:

    mmlsfs all

Mounting the distributed FS (be sure to pass -a so that the filesystem is mounted on all nodes):

    mmmount all -a

All done.  Now you should be able to go to the mounted FS:

    cd /gpfs/gpfsfpo

.. and see that there's 300 G there:

    [root@gpfs1 gpfsfpo]# df -h .
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/gpfsfpo     300G  678M   300G   1% /gpfs/gpfsfpo

Make sure you can write, e.g.

    touch aa

If the file was created, you are all set:

    ls -l /gpfs/gpfsfpo
    ssh gpfs2 'ls -l /gpfs/gpfsfpo'
    ssh gpfs3 'ls -l /gpfs/gpfsfpo'


# Part 2 - LazyNLP [Crawler library](https://github.com/MIDS-scaling-up/v2/blob/master/week12/hw/dataset.md)
