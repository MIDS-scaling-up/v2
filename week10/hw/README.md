# [IS BEING REVISED PLEASE DO NOT START THIS YET] OpenAI Gym Framework

OpenAI Gym is a framework that allows developing, training and testing of learning agents; one of it's applications is reinforcement learning, during this homework we will experiment with a Jupyter notebook aiming to train an agent to play a game using Reinforcement learning and Deep Learning.

## Anaconda and OpenAI Gym installation
These set of instructions is intended to be run in your local station (MAC OS X, or Windows)
1. Install Anaconda according to [installation](https://docs.anaconda.com/anaconda/install/mac-os/)

2. Update the local environment with the frameworks to support OpenAI Gym and launch the Jupyter notebook environmet
```
conda create -n week10 python=3.7 ipykernel jupyter anaconda
source activate week10
ipython kernel install --name week10 --user
pip install gym
pip install keras
pip install tensorflow
conda install ipykernel
python -m ipykernel install --user --name week10 --display-name "Python week10"
jupyter notebook

```
3. Run the attached playbook and document your results, experiment with settings in the model creation, training data and initial random game, annotate your observations.

## Submission
Submit a document with evidence of the playbook run, changes you made and observations.
