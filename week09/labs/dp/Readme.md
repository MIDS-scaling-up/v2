# Lab 9: Fun with distributed model training in Pytorch


### 1. In AWS, ~~get a VM with two GPUs~~ Use the pre-created jupyter lab URL created by your instructors
Make sure port 8888 is exposed, ssh your VM.


Start the lab09 docker container in interactive mode:
```

# Assuming your external hard drive is mounted in /data, pass it through using -v
docker run --rm --gpus all -v /data2:/data -p 8888:8888 --ipc=host -ti w251/lab09 bash
# Then, start Jupyter as
jupyter lab --ip=0.0.0.0 --allow-root
```
Note the token that it prints and connect to it via browser at `http://vm_ip:8888`


### 2. Distributed Data Parallel
Upload [the python notebook](https://github.com/MIDS-scaling-up/v2/blob/master/week09/labs/dp/BERT_classifying_toxicity_dp_lab.ipynb) to your server. 
1. Review it and remind yourself what it's about
1. Run through it - as is it should run on one GPU - and make sure it runs. Choose a small subset of data so it won't take forever. Note how long it takes to complete
1. Using [PyTorch DataParallel](https://pytorch.org/docs/stable/generated/torch.nn.DataParallel.html) make sure your model is placed on both GPUs
1. Run through the training code. How long does it take now?
1. Same for the inference code.  What is the speedup?

### 3a. Distributed Data Parallel - single node
Upload the [python file](https://github.com/MIDS-scaling-up/v2/blob/master/week09/labs/dp/toxicity_ddp_lab.py) to your VM.
1. Review it and make sure you still recognize it. It's the same logic, slightly repackaged
1. Remind yourself, how do you properly run distributed workloads? What do you use for coordination?
1. Run through it - as it it should run on just one GPU.  How do you properly run it ?  how long does the training take?
1. Now, use [Pytorch DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html) to (a) create a distributed data sampler and (b) do distributed training. How long does it take now?

### 3b. Distributed Data Parallel - multi node
This is a more advanced lab that will require additional preparation.
1. We will need a pair of GPU VMs - we recommend g4dn.xlarge as they are the cheapest
2. When you provision them, make sure they are in the same VPC, and follow the same general instructions in homework 9 - e.g. make sure that between these VMs, all ports are open. This is needed for communication between them
3. Launch the containers just like we did in homework 9, e.g. docker run --gpus all -d --name group --net=host -e SSH_PORT=4444 w251/lab09:mn
4. Now, create an interactive shell inside each container, e.g. docker exec -ti group bash
5. In each container, download the data, e.g. `cd /workspace/v2/week09/labs/dp && sh data.sh`
6. You will need to make further changes to the python script now.  You will need to make sure that the MASTER_ADDR environment variable is passed through.  You will need to make sure that the model is always placed on GPU 0 (since you have only one GPU in the system now). 
7. Run the script. For instance:

```
mpirun --allow-run-as-root -n 2 -H 172.31.11.31:1,172.31.5.11:1 -bind-to none -map-by slot --mca btl_tcp_if_include ens5 -x NCCL_SOCKET_IFNAME=ens5 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x MASTER_ADDR=172.31.11.31 /opt/conda/bin/python /workspace/v2/week09/labs/dp/toxicity_ddp.py
```
