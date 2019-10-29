# Homework 11 -- More fun with OpenAI Gym!

In this homework, you will be training a Lunar Lander to land properly **using your Jetson TX2**. There is a video component to this file, so use a display or VNC.

There are two python scripts used for this process. The first file, `lunar_lander.py`, defines the Lunar Lander for OpenAI Gym. It also defines the keras model.

The second file, `run_lunar_lander.py`, instantiates the Lunar Lander environment and runs it.

The code that creates the model in `lunar_lander.py` is:

```
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model
```
 
In its current state, the model which is created is not very good.

For this homework, you should adjust the model parameters and the training parameters (total iterations and threshold) to get better results. You should do a little research into how the parameters affect the resulting model. For example, is `adam` better than `adamax`?

You should try at least three different configurations (one can be the initial "base" configuration) and compare your results. The goal is to increase the number of successful landings (noted by the output "Landed it!").

The training parameters are in the `run_lunar_lander.py` file:

```
.
.
.
    model = nnmodel(10)

.
.
.
    training_thr = 3000
    total_itrs = 50000
.
.
.
        if steps > training_thr and steps %1000 ==0:
            # re-train a model
            print("training model model")
            modelTrained = True
            model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 10, batch_size=20)
.
.
.

``` 

To run the environment, use these commands (ensure you have all the files from the hw11 github folder in your current directory):

```
sudo docker build -t lander -f Dockerfile.lander .
xhost +
sudo docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /tmp/videos:/tmp/videos lander
```

You will have a lot of mp4 files in `/tmp/videos` on your TX2. You can use VLC to watch the videos of your landing attempts to see the improvement of your model over the iterations.

## To Turn In
You should upload two or three videos showing your best model to Cloud Object Storage and provide links using the instructions below.

Also, submit a write-up of the tweaks you made to the model and the effect they had on the results. What parameters did you change? Did they improve or degrade the model?

We will compare results in class.


#### Enable http access to Cloud Object Storage

```
Here's how to enable http access to the S3 COS:
1) create a bucket & upload a file, remember the resiliency you pick and the location
2) Go to Buckets -> Access Policies -> Public Access
3) click the "Create access policy" button
4) Go to Endpoint (on the left menu) and select your resiliency to find your endpoint (mine was "Regional" because that's how I created my COS)
5) Your endpoint is the Public location plus your bucket name plus the file

Example: https://s3.eu-gb.cloud-object-storage.appdomain.cloud/brooklyn-artifacts/IBM_MULTICLOUD_MANAGER_3.1.2_KLUS.tar.gz

In this example, the bucket is "brooklyn-artifacts" and the single Region is eu-gb
```