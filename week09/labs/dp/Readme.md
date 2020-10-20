# Lab 9: Fun with distributed model training in Pytorch


### 1. In AWS, get a VM with two GPUs
Make sure port 8888 is exposed, ssh into the VM.
### 2. Distributed Data Parallel

Start the lab09 docker container in interactive mode:
```

# Assuming your external hard drive is mounted in /data, pass it through using -v
docker run --rm --gpus all -v /data2:/data -p 8888:8888 --ipc=host -ti w251/lab09 bash
# Then, start Jupyter as
jupyter lab --ip=0.0.0.0 --allow-root
```
