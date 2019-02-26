# Homework 9: HPC

### Get a pair of GPU VMs in Softlayer
Follow instructions in [Homework 3](https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw) to get a pair of VMs in Softlayer.  Call them, for instance, p100a and p100b.  Install cuda, docker , nvidia-docker, format the 2TB drive and mount it to /data

### Create containers for openseq2seq

1. Create account at https://ngc.nvidia.com/
1. Follow [this instruction](https://docs.nvidia.com/ngc/ngc-getting-started-guide/index.html#generating-api-key) to create Nvidia Cloud docker registry API Key
1. Login into one of the VMs and use your API key to login into Nvidia Cloud docker registry
1. Pull the latest tensorflow image: ```docker pull nvcr.io/nvidia/tensorflow:19.01-py```
1. Use files on [docker directory](docker) to create an openseq2seq image 
1. Copy image to the other VM 
1. Create containers on both VMs: ``` docker run --runtime=nvidia -d --name openseq2seq --net=host -e SSH_PORT=4444 -v /data:/data openseq2seq ```
1. On both VMs create an interactive bash seesion inside the container: ``` docker exec -ti openseq2seq bash ``` and run the follwoing commands in the container shell:
    1. Test mpi: ``` mpirun -n 2 -H <vm1 private ip address>,<vm2 private ip address> --allow-run-as-root hostname ``` 
    1. Pull data to be used in neural machine tranlsation training ([more info](https://nvidia.github.io/OpenSeq2Seq/html/machine-translation.html)):  
    ``` 
    cd /opt/OpenSeq2seq 
    scripts/get_en_de.sh /data/wmt16_de_en
    ```
    1. Copy configuration file to /data directory: ``` cp example_configs/text2text/en-de/en-de-nmt-small.py /data ``
    1. Edit /data/en-de-nmt-small.py to replace ```[REPLACE THIS TO THE PATH WITH YOUR WMT DATA]``` with ```/data/wmt16_de_en``` and in base_parms section replace ```"logdir": "nmt-small-en-de",``` with ```"logdir": "/data/nmt-small-en-de",```
    1. Start training -- **on one VM only:** ```nohup mpirun --allow-run-as-root -n 4 -H <vm1 private ip address>:2,<vm2 private ip address>:2 -bind-to none -map-by slot --mca btl_tcp_if_include eth0  -x NCCL_SOCKET_IFNAME=eth0 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH  python run.py --config_file=/data/en-de-nmt-small.py --use_horovod=True --mode=train_eval & ```
    1. Monitor training progress: ``` tail -f nohup,out ```

### Submission

Please submit the nohup.out file.
