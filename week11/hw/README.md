# Homework 11: Robotics and Deep Reinforcement Learning

Prereq: Work through the demos from Dusty:
https://github.com/dusty-nv/jetson-reinforcement

### Note: 
You will need to modify Dusty's files with the following steps. Run these before running the cmake command in the original instructions.

```
pip uninstall torchvision
cd jetson-reinforcement/build/pytorch
mv vision /tmp
git clone -b v0.2.0 https://github.com/pytorch/vision
cd vision
sudo python setup.py install
```

These demos will give you a taste for running DRL frameworks on your TX2.

Assignment: Create a quadruped robot in Gazebo that consists of torso with four cylindrical legs. Each leg is attached to the torso with a revolute joint.

Then create a new robot vehicle which has six wheels and a scoop front loading mechanism.

Gazebo reference:  
 - http://gazebosim.org/tutorials?cat=build_robot
 - https://bitbucket.org/osrf/gazebo_models/src

## To Turn In
Turn in screen recordings of your two robots in action
