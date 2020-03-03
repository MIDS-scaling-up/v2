# THIS HOMEWORK IS BEING POSTPONED,PLEASE FOCUS IN YOUR WEEK 10 PROJECT UPDATE PRESENTATION.










OpenAI Gym Framework

OpenAI Gym is a framework that allows developing, training and testing of learning agents; one of it's applications is reinforcement learning, during this homework we will experiment with a Jupyter notebook aiming to train an agent to play a game using Reinforcement learning and Deep Learning.

OpenAI provides a common python interface to interact with the standarized set of environments, it is compatible with computational libraries liuke TensorFlow or Theano.

There are two basic concepts in reinforcement learning: the environment and the agent. The agent sends actions to the environment, and the environment replies with observations and rewards (that is, a score).

# General steps 
1. reset(self): Reset the environment's state. Returns observation.
2. step(self, action): Step the environment by one timestep. Returns observation, reward, done, info.
3. render(self, mode='human'): Render one frame of the environment. The default mode will do something human friendly, such as pop up a window.

More information [Gym getting started](https://gym.openai.com/docs/)


## Dockerfile instructions example
```
clone the github repo including the Docker file and the gym.ipynb in the same directory
 
Build the docker file: docker build -t gym .
Run it: docker run --name gymweek10 -d -p 8888:8888 -p 6006:6006 gym:latest
Access the Jupyter notebook endpoint: http://XX.XX.XX.XX:8888/tree?  (tip look for docker logs containerID to get the token)
Run the gym.ipynb Notebook annotate your results 
```

## Docker pull instructions
```
docker pull eariasn/w251-eariasn:hw10
Run it: docker run --name gymweek10 -d -p 8888:8888 -p 6006:6006 eariasn/w251-eariasn:hw10
Access the Jupyter notebook endpoint: http://XX.XX.XX.XX:8888/tree?  (tip look for docker logs containerID to get the token)
Run the gym.ipynb Notebook annotate your results

```
## Submission
Submit a document with evidence of the playbook run, changes you made and observations.


