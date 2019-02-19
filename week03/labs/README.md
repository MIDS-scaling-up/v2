# Labs 3: Fun with Digits on the Jetson

Digits is an [Open Source](https://github.com/NVIDIA/DIGITS) project by Nvidia, designed to make it easy to train neural networks.

## Setting Up the Jetson for DIGITS (Optional)

If you haven't done this already, on your TX2, go to the directory where you cloned homework3 (e.g. v2/week03/hw ) and examine Dockerfile.caffebase, the docker file for Nvidia Caffe.  Once you are done looking it over, build the docker image:
```
docker build -t caffe -f Dockerfile.caffebase .
```
This obviously assumes that you completed previous homeworks and already created a docker image called "cudabase" and that it exists locally. This build will take some time.  If for some reason this fails, you could cheat and pull the already created image from the class docker hub repo: 
```
docker pull w251/nvcaffe:tx2-3.3_b39
```

You should now have your NVCaffe container for the Jetson TX2 all ready to go!

### Running DIGITS in a container on the Jetson
Familiarize yourself with the Dockefile.digits container.  Note the FROM clause and modify it if needed. Assuming you already have the Caffe image built or downloaded, build the DIGITS image now:
```
docker build -t digits -f Dockerfile.digits .
```
Once again, if something goes terribly wrong, you can use our pre-built container instead:
```
docker pull w251/digits:tx2-3.3_b39
```

When you run DIGITS, you likely want to pass your data directory through so you won't be copying enormous data sets back and forth.  If you recall, we asked you to add a larger storage device to your Jetson.  Assuming it's mounted to /data, do something like this:
```
mkdir -m 777 /data/digits-data
```

Now, run the DIGITS container, passing your data dir as /data and using host port 5001:
```
docker run --privileged -v /data/digits-data:/data -p 5001:5001 -d digits
```
Open a browser window and go to localhost:5001 to access DIGITS running on the Jetson. If you need to add large files (such as pre-trained models or datasets), copy them to /data/digits-data on the host and they will be visible under /data on the Jetson.

