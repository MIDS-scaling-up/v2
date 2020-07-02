# Homework 11 -- More fun with OpenAI Gym!

In this homework, you will be training a Lunar Lander module to land properly **using your Jetson TX2**. There is a video component to this file, so use a display or VNC.

First, some background reading: https://www.novatec-gmbh.de/en/blog/introduction-to-q-learning/

We are using a container base image with all the OpenAI Gym prerequisites installed. 

The python code is in agent_lunar_lander.py.

In the python code, the `env.step()` method directs the lander module to take another step (equivalent to one frame of video) and returns several fields: `state`, `reward`, `done`, and `info`. 

 - The `state` is a vector with eight values (x and y position, x and y velocity, lander angle and angular velocity, boolean for left leg contact with ground, boolean for right leg contact with ground). The state information is used to build the model using Keras.
 - The `reward` is a value indicating whether or not the step was "good" or "bad". A reward greater than 200 indicates a successful landing.
 - The `done` field is a boolean indicating whether or not the module has landed. 
 - `info` is not used.

The goal of this homework is to train the lunar module to land better. The model, as it is currently configured, will not converge and the lunar module will never learn to land well. By modifying the parameters (lines 30-43 of the python code), you should be able to train the module in fewer than 500 iterations.

```
        self.density_first_layer = 16
        self.density_second_layer = 8
        self.num_epochs = 1
        self.batch_size = 64
        self.epsilon_min = 0.01
```

We are using a Sequential model for the lander. A Sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor (current state) and one output tensor (best move to make). The "moves" that can be made are firing the thrusters (right, left, up) to adjust the speed and trajectory.

The current model has three layers. Consider the dimension of the input tensor for each layer. Is it optimal? Are the activations appropriate for the use case?

```
        model = Sequential()
        model.add(Dense(self.density_first_layer, input_dim=self.num_observation_space, activation=relu))
        model.add(Dense(self.density_second_layer, activation=relu))
        model.add(Dense(self.num_action_space, activation=linear))
```

To run the environment, use these commands (ensure you have all the files from the hw11 github folder in your current directory on the TX2):

```
# If you haven't added your User to the docker group, do it now
sudo usermod -aG docker $USER

# reboot to make the previous step take effect

docker build -t hw11 -f Dockerfile.agent .

# enable video sharing from the container
xhost +

# maximize performance on the device
sudo jetson_clocks --store
sudo jetson_clocks
time docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /data/videos:/tmp/videos hw11

# don't forget to turn off the fan on the device
sudo jetson_clocks --restore
```

When the process starts, you will see the animation of the lunar lander on your screen and the training will start.

Training output looks like this:

```
0 	: Episode || Reward:  -355.4552185273774 	|| Average Reward:  -355.4552185273774 	 epsilon:  0.995
1 	: Episode || Reward:  -302.69548515410156 	|| Average Reward:  -329.0753518407395 	 epsilon:  0.990025
2 	: Episode || Reward:  -197.1461440026914 	|| Average Reward:  -285.09894922805677 	 epsilon:  0.985074875
3 	: Episode || Reward:  -251.29447991556844 	|| Average Reward:  -276.64783189993466 	 epsilon:  0.9801495006250001
4 	: Episode || Reward:  -312.69842116384507 	|| Average Reward:  -283.85794975271676 	 epsilon:  0.9752487531218751
5 	: Episode || Reward:  -193.10620553981315 	|| Average Reward:  -268.73265905056616 	 epsilon:  0.9703725093562657
6 	: Episode || Reward:  -125.35339813322857 	|| Average Reward:  -248.2499074909465 	 epsilon:  0.9655206468094844
7 	: Episode || Reward:  -95.87496167296544 	|| Average Reward:  -229.20303926369886 	 epsilon:  0.960693043575437
8 	: Episode || Reward:  -10.731355125180073 	|| Average Reward:  -204.92840769275233 	 epsilon:  0.9558895783575597
```

The training will end when either the Average Reward is greater than 200, or 2000 iterations have passed. I would recommend killing the model if it ever hits 800, though.

After the training, it will run a test process. The output will look like this:

```
DQN Training Complete...
Starting Testing of the trained model...
0       : Episode || Reward:  219.64614710147364
1       : Episode || Reward:  204.5401595978414
2       : Episode || Reward:  191.82778586724473
3       : Episode || Reward:  300.26513457499857
4       : Episode || Reward:  265.38375246986914
5       : Episode || Reward:  231.17971859331598
6       : Episode || Reward:  158.1286447553571
.
.
.
Average Reward:  243.09916996497867
```

**The assignment**: Modify the parameters with your best (educated) guess to improve the model training. A well tuned model will start landing the module after about 300 iterations and consistently land it after about 400 iterations. If you are feeling creative, you can change other aspects of the model training (like batch size and epsilon value).

**Each training run will take between 150 and 400 minutes**. So it is recommended to kick off the container and come back later to check on it. Try running the training process a few times with different values.

You will have a lot of mp4 files in `/data/videos` on your TX2. You can use VLC or Chrome to watch the videos of your landing attempts to see the improvement of your model over the iterations.

## To Turn In
You should save three videos showing your first, last, and an intermediary run of the training. Also save a couple videos from the testing process that runs at the end of the training.

Upload all the videos to Cloud Object Storage and provide links using the instructions below.

Submit a write-up of the tweaks you made to the model and the effect they had on the results. 
Questions to answer:
1) What parameters did you change? 
2) What values did you try?
3) Did you try any other changes that made things better or worse?
4) Did they improve or degrade the model? Did you have a test run with 100% of the scores above 200?
5) Based on what you observed, what conclusions can you draw about the different parameters and their values? 
6) What is the purpose of the epsilon value?
7) Describe "Q-Learning".

## Grading is based on the changes made and the observed output, not on the accuracy of the model.

We will compare results in class. The biggest Average Reward after the test run "wins":

```
Average Reward:  243.09916996497867
```

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
