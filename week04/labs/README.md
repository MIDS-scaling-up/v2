### This lab will follow on from the homework and build a 1d-CNN

#### Ordering an instance from the image template you built in week02
Login to your ibmcloud `ibmcloud login`  
Please order a p100 virtual server off an existing w251 image.   
For example, I ran the following:
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100 --domain=darragh.com  --flavor AC1_8X60X25 --billing=hourly --san  --network 1000 --image 2208861 --key=1418191
```
You will need to change the fields : `key`, and optionally the `datacenter`, `domain` and `hostname`.
  
Please wait a minute or two for the VM to be created. Your can check it's status by running:
`ibmcloud sl vs list`  

Now login, I logged in like below, where I entered my public key location, and the VM IP.  
`ssh -i /home/darragh/.ssh/id_rsa 158.176.93.70 -l root`

#### Start the Jupyter notebook.

When logged in to your VM, lets build our docker with the jupyter notebook.  
Once in, start running your notebook and follow the instructions in bold where to fill in code. 
```
docker run --rm --runtime=nvidia -it -p 8888:8888 w251/tensorflow_gpu_lab04:latest
```
