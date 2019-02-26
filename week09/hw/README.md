# Homework 9: HPC

### Get a pair of GPU VMs in Softlayer
Follow instructions in [Homework 3](https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw) to get a pair of VMs in Softlayer.  Call them, for instance, p100a and p100b.

### Create containers for openseq2seq

1. Create account at https://ngc.nvidia.com/
1. Follow [this instruction](https://docs.nvidia.com/ngc/ngc-getting-started-guide/index.html#generating-api-key) to create Nvidia Cloud docker registry API Key
1. Login to one ov the VMs and use your API key to login into Nvidia Cloud docker registry
1. Pull the latest tensorflow image: ```docker pull nvcr.io/nvidia/tensorflow:19.01-py```
1. Use files on [docker directory](docker) to create an image 

