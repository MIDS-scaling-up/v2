### OpenAI Gym fun

Basics
======

There are two basic concepts in reinforcement learning: the
environment (namely, the outside world) and the agent (namely, the
algorithm you are writing). The agent sends `actions` to the
environment, and the environment replies with `observations` and
`rewards` (that is, a score).

The core `gym` interface is [Env](https://github.com/openai/gym/blob/master/gym/core.py), which is
the unified environment interface. There is no interface for agents;
that part is left to you. The following are the ``Env`` methods you
should know:

- `reset(self)`: Reset the environment's state. Returns `observation`.
- `step(self, action)`: Step the environment by one timestep. Returns `observation`, `reward`, `done`, `info`.
- `render(self, mode='human')`: Render one frame of the environment. The default mode will do something human friendly, such as pop up a window. 
AWS setup
============
Order an t3a.xlarge instance with the deep learning ami using one security group that would allow you to connect to port 8888 with a public IP address, similar to this (replace values as appropiate)

```
aws ec2 run-instances --image-id ami-01aad86525617098d --instance-type t3a.xlarge --security-group-ids sg-0a53b2b5dd9742d84  --associate-public-ip-address --key-name eariasn --count 1
```
Connect into the instance and checkout this docker image:

```
docker pull jaimeps/rl-gym
docker run -d -p 8888:8888 jaimeps/rl-gym
docker logs docker-id (to get the token for the python notebook)
```

## Example notebook

Using the Jupyter notebook Docker image, proceed to open the attached notebook lab1.ipynb and follow along the code with the instructors help. Feel free to the second notebook gym.ipynb

## Cancel the instance after you are done.


