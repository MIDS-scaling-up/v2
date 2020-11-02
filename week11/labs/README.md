# AWS DeepRacer Lab -- Start at the beginning of class to allow 60 minutes to train the model
In this lab, we will look at the AWS DeepRacer project. You will design a Reinforcement Learning training program for a virtual car on a virtual track by tweaking parameters like steering and speed.

First, go to the [DeepRacer portal](https://console.aws.amazon.com/deepracer/home?region=us-east-1).

## Step 0
Go to the "Get started" link

You will see a button to create all the required resources:

![](GetStarted.png)

## Step 1
Learn the basics of reinforcement learning (Required / ~10 mins)

![](StartLearningRL.png)

**You can skip this step because we will discuss in class.**

## Step 2
Create a model and race (Required / ~1 hour)

![](CreateModel.png)

Click the "Create Model" button and fill out the details:

 - Model name
 - Environment Simulation **Pick the re:Invent 2018 track for this lab**
 - Race type: Time trial
 - Agent: `The Original DeepRacer`
 - Pick a reward function (based on what you learned in the "basics" walkthrough)
 - Use the default Hyperparameters
 - Use the default stop condition of 60 minutes


## Start your training
Click the button to `Create Model` which will start the training
 
## Check your results
After the training is complete, run an evaluation of the model. 

 - How far did your car go? 
 - Compare your results to others. 
 - Did you change any parameters that made your model perform better or worse? 
 - Does your car run very well on other tracks?

## Fun Links:
 - [AWS Racer Reward function inputs](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html)
 - [Huber loss](https://en.wikipedia.org/wiki/Huber_loss)
 - [Proximal Policy Optimization](https://arxiv.org/pdf/1707.06347.pdf) and [AWS Racer Primer on PPO](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-how-it-works-reinforcement-learning-algorithm.html)
 
