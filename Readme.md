# HW 4: Jetson-Reinforcement 

Reinforcement learning is an area of machine learning that plays a large role in robotics. The primary focus of reinforcement learning is the agent, which is the software commanding the robot and running the tasks. These agents gather experience when in action and strive for results to maximize some determined reward system. This training style can prepare robots for complex, intuitive tasks. In this week's homwork, we'll set up some reinforcement learning environments on the Jetson. The theory is to train simulated 3D agents that can be transfered to a real robot.

## Setting up Reinforcement on the Jetson

As usual, we will set up a Docker container with these reinforcement learning environments. This will include a PyTorch setup with Deep-Q Learning, A3G algorithms, and a C++ API to allow integration with robots and simulators. 

### Building the Reinforcement Docker Container

Before building the Reinforcement image, we first need a suitable caffe image. The previous caffe image we made is incompatible with the Reinforcement libraries, so download the Dockerfile.caffealt file and build a new caffealt image:
```
docker build -t caffealt -f Dockerfile.caffealt .
```
Now with the alternative caffe image built, download the Dockerfile.reinforce file and build the reinforcement image:
```
docker build -t reinforcement -f Dockerfile.reinforce .
```
When running the container, make sure to enable X so that the container can open windows when running the reinforcement learning environments:
```
xhost +
docker run --privileged -v /dev:/dev -e DISPLAY=$DISPLAY -v /tmp:tmp --net=host --ipc=host --ti -p 8888:8888 reinforcement
```

### Testing PyTorch

PyTorch is a machine learning library for Python that is based on Torch. PyTorch is included in the Reinforcement image, so let's test to see if it is properly installed and has CUDA/cuDNN support. While inside the Reinforcement container, enter a Python shell by running `python` in the command line. Then, test out pytorch:
```
>>> import pytorch
>>> print(torch.__version__)
```
The shell should print out nothing for the first command, and `0.3.0b0+af3964a` (or something similar) for the second command. Now test CUDA:
```
>>> print('CUDA available: ' + str(torch.cuda.is_available()))
>>> a = torch.cuda.FloatTensor(2).zero_()
>>> print('Tensor a = ' + str(a))
```
The first command simply tells you if CUDA is available, while the second performs a simple operation with a tensor allocated on the GPU. The output for this operation should be as follows (the calculation may take some time):
```
Tensor a = 
 0
 0
[torch.cuda.FloatTensor of size 2 (GPU 0)]
```

## Running Reinforcement Learning Examples

The Reinforcement container has many examples for reinforcement learning. The full documentation includes the list of all included examples with detailed descrptions here: https://github.com/dusty-nv/jetson-reinforcement. For the homework, we'll focus on the more complex simulations. 

### 3D Robotic Gazebo Simulations

The Reinforcement container includes the Gazebo robotic simulator. We will run two simulations on Gazebo, a robotic arm and a rover. First, navigate to the `/jetson-reinforcement/build/aarch64/bin` directory. Run the robotic arm simulation, which has an arm (which is the "agent" component in reinforcement learning) attempt to find a target object (which is the "reward" component in reinforcement learning):
```
./gazebo-arm.sh
```
You should see something like this (it might take a while to load):
<img src="https://raw.githubusercontent.com/dusty-nv/jetson-reinforcement/master/docs/images/gazebo_arm.jpg">

Watch how the arm tries to find the object. Once it starts getting consistently close to the object, you can start moving the object around by pressing `t` to enter "Translation" mode and clicking and dragging the object. Note the arm can only rotate 45 degrees in either direction, so keep the object within the arm's range.

Once you've played around with the arm simulation, you can move on to the rover simulation. The rover attempts to find the object while also avoiding the walls of the environment:
```
./gazebo-rover.sh
```
The rover simulation looks like this:
<img src="https://raw.githubusercontent.com/dusty-nv/jetson-reinforcement/master/docs/images/gazebo_rover.jpg">

Like the arm, once the rover starts finding the object consistently then you can move the target object in the same way as in the arm simulation.

## Bonus: Jupyter Examples

The Reinforcement container also includes a handy Jupyter notebook with several examples built in. To explore these, navigate to `/jetson-reinforcement/build/aarch64/bin` and run the following command:
```
jupyter-notebook --ip 0.0.0.0 --no-browser --allow-root intro-pytorch.ipynb
```
Follow the prompted instructions to access the notebook via your browser and poke around. The `intro-pytorch.ipynb` and `intro-DQN.ipynb` are good starting points (hint: click on a block of code and use CTRL+Enter keys to run the code).
