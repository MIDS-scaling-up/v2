# Kaggle labs

### Provision your VM
We recommmend that you provision a VM with a V-100 GPU in Dallas 12 this time. This is because we placed our dataset into an object storage pod in US South.
```
slcli vs create --datacenter=dal12 --hostname=v100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=p305 --flavor AC2_8X60X100 --san
```

### Mount the object storage bucket.  
Note that we created an object storage bucket in the US South availability zone and are providing read only credentials to you.
```
# create the mountpoint
mkdir -m 777 /week07
# install the s3fs mount utility
apt update && apt install -y s3fs
# save the read only creds
echo "3fb8e3920adf45f38d51b813ed064544:650bdf1dfb0d0e8ddb91e34ab9758cf7b9c8ca957988fe52" > ~/root/.cos_creds
# this file needs to be secure
chmod 600 ~/root/.cos_creds
# mount it
s3fs w251dal /week07 -o passwd_file=/root/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.private.us-south.cloud-object-storage.appdomain.cloud -o nonempty
```
### Start the docker container with jupyter inside
Make sure to pass the mountpoint
```
# start it.
docker run --runtime=nvidia --ipc=host --rm -v /week07:/data -p 8888:8888 -d w251/lab07
# get the token
docker logs <container id>
```
Now you can connect to your jupyter at ```http://ip_of_your_vm:8888?token=yourtoken````
