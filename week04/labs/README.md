### This lab will follow on from the homework and build a 1d-CNN

#### Running locally on the Jetson
The Jetson's small GPU has 256 cores, here's how to put it through its paces.  Note that we use the container for the Jetson here, not for the cloud; these containers differ!

```
# start the container:
root@dima-desktop:~/v2/backup/keras# docker run --rm --privileged -p 8888:8888 -d  w251/tensorflow_gpu_lab04:dev-tx2-4.2.1_b97-py3 
67ad13ba7dfb8a58c048dec4d5fec3d3f3c9c52eee6d18d9c5c65debf0d06d51

# Use the container id above and grab the token:
root@dima-desktop:~/v2/backup/keras# docker logs 67ad13ba7dfb8a58c048dec4d5fec3d3f3c9c52eee6d18d9c5c65debf0d06d51
[I 16:31:50.951 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 16:31:51.970 NotebookApp] Serving notebooks from local directory: /notebooks
[I 16:31:51.971 NotebookApp] The Jupyter Notebook is running at:
[I 16:31:51.972 NotebookApp] http://67ad13ba7dfb:8888/?token=1db35ebea1544348a44772bc8b9ae101405fed1f658c912d
[I 16:31:51.972 NotebookApp]  or http://127.0.0.1:8888/?token=1db35ebea1544348a44772bc8b9ae101405fed1f658c912d
[I 16:31:51.972 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```
You can now access your notebook at http://yourjetsonip:8888?token=yourtoken

#### Ordering an instance from the image template you built in week02
Login to your ibmcloud `ibmcloud login`  
Please order a p100 virtual server off an existing w251 image. If you have trouble starting from your image, use ours image number 2250329 (see below). You will need to use your key, though.

For example, I ran the following:
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100 --domain=darragh.com  --flavor AC1_8X60X25 --billing=hourly --san  --network 1000 --image 2250329 --key=1418191
```
You will need to change the fields : `key`, and optionally the `datacenter`, `domain` and `hostname`.
  
Please wait a minute or two for the VM to be created. Your can check it's status by running:
`ibmcloud sl vs list`  

Now login, I logged in like below, where I entered my public key location, and the VM IP.  
`ssh -i /home/darragh/.ssh/id_rsa 158.176.93.70 -l root`

#### Start the Jupyter notebook.

When logged in to your VM, lets build our docker with the jupyter notebook. Make sure that we use our cloud container, not the Jetson container. 
Once in, start running your notebook and follow the instructions in bold where to fill in code.  
```
docker run --rm --runtime=nvidia -it -p 8888:8888 w251/tensorflow_gpu_lab04:latest
```

This docker run will open a jupyter notebook, and the token will be provided on output of the docker run. You can reach this by going in your browser to `http://<my_ip>:8888`.  

For example, for my notebook, I go to `http://158.176.93.70:8888`, and enter my token.   

#### Don't forget to CANCEL (not shut down but CANCEL) this VM after you are done to avoid a continuous charge!
