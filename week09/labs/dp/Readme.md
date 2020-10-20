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

### 3. Distributed Data Parallel
Upload the [python file](https://github.com/MIDS-scaling-up/v2/blob/master/week09/labs/dp/toxicity_ddp_lab.py) to your VM.
1. Review it and make sure you still recognize it. It's the same logic, slightly repackaged
1. Remind yourself, how do you properly run distributed workloads? What do you use for coordination?
1. Run through it - as it it should run on just one GPU.  How do you properly run it ?  how long does the training take?
1. Now, use [Pytorch DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html) to (a) create a distributed data sampler and (b) do distributed training. How long does it take now?
