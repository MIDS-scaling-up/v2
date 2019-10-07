# Kaggle labs

### Provision your VM
We recommmend that you provision a VM with a V-100 GPU in Dallas 12 this time. This is because we placed our dataset into an object storage pod in US South.
```
slcli vs create --datacenter=dal12 --hostname=v100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=p305 --flavor AC2_8X60X100 --san
```

### Mount our object storage bucket.  Note that we are providing read only credentials to you.
```
mkdir -m 777 /week07
apt update && apt install -y s3fs
# read only creds
echo "3fb8e3920adf45f38d51b813ed064544:650bdf1dfb0d0e8ddb91e34ab9758cf7b9c8ca957988fe52" > ~/root/.cos_creds
chmod 600 ~/root/.cos_creds
s3fs w251dal /week07 -o passwd_file=/root/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.private.us-south.cloud-object-storage.appdomain.cloud -o nonempty
```
