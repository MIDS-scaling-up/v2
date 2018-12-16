## Base cuda container for Xavier Jetpack 4.1.1

### Building the runtime container
Simply do this
```
docker build -t cudabase -f Dockerfile.cudabase .
```

### Running
We are not installing the drivers inside the container to save space.  So, to run the container, you will need to pass the driver directory:
```
docker run --rm --privileged -v /usr/lib/aarch64-linux-gnu:/usr/lib/aarch64-linux-gnu -ti cudabase bash
```

### Building the dev container
The dev container must have the required libraries inside so you can use it as the base.  So, the process is a little more involved under the hood. We tar up /usr/lib/aarch64-linux-gnu and simply copy it to the container.  Note that we are using libglvnd to avoid versioning conflicts with LibGL.  So,
```
sh build.sh
```
This should create cudabase:dev, which you should use as the base going forward
