import sys, math
import numpy as np

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)

import gym
from gym import spaces
from gym.utils import seeding
import skvideo.io
from keras.models import Sequential
from keras.layers import Dense
from lunar_lander import *

# Initialize training data
X_train, y_train = [],[]
frames = []

if __name__=="__main__":
    # Initialize lunar lander environment
    env = LunarLanderContinuous()

    steps = 0
    # Initialize the model
    model = nnmodel(10)
    total_reward = 0
    prev_reward = 0
    training_thr = 50 # 5000
    total_itrs = 500 # 5000
    num_steps = 10 # 1000
    mid_episode_training = 1000
    unsuccessful_landing = 0
    successful_steps = []
    modelTrained = False
    local_iterations = 0

    # Run through total_itrs episodes
    while steps <= total_itrs:
        prev_state = env.reset()
        done = False
        total_reward = 0

        action = np.array([0.0,0.0])

        # This loop stays active during the whole duration of one episode
        while not done:

            if modelTrained:
                max_reward = -1000
                max_action = None

                # Get 100 predictions for the next step
                # and pick the one with the max reward potential
                for i in range(100):
                    action1 = np.random.randint(-1000,1000)/1000
                    action2 = np.random.randint(-1000,1000)/1000
                    test_action = [action1,action2]
                    reward_prediction = model.predict(np.array(list(new_state)+list(test_action)).reshape(1,len(list(new_state)+list(test_action))), workers=100, use_multiprocessing=True)
                    if reward_prediction > max_reward:
                        max_reward = reward_prediction
                        max_action = test_action

                # Set the action for the next iteration
                action = np.array(max_action)
            else:
                action = np.array([np.random.randint(-1000,1000)/1000, np.random.randint(-1000,1000)/1000])

            #Take another step in the environment
            new_state, reward, done, info = env.step(action)

            # X_train remembers the actions
            X_train.append(list(new_state)+list(action))

            # y_train remembers the reward for each action
            y_train.append(reward)

            prev_state = new_state
            prev_reward = reward

            if done:
                if prev_reward >= 200:
                    successful_steps.append(steps)
                    print("Successful Landing!!! ",steps)
                    print("Total successes are: ", len(successful_steps))
                else: 
                    unsuccessful_landing += 1

            total_reward += reward

            if reward > 100:
                print("Decent move")

            # If we are spinning out of control, give up and try again
            #if (total_reward < -500 or local_iterations > 1000):
            #    done = True

            local_iterations += 1

            if steps >= training_thr and local_iterations % mid_episode_training ==0 and not done:
                # re-train a model
                print("Training model mid-episode.")
                modelTrained = True
                model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 10, batch_size=32, workers=100, use_multiprocessing=True)


            #steps += 1
            #if steps >= 15000:
            #    frame = env.render(mode='rgb_array')
            #    frames.append(frame)
            #    if steps >= training_thr and steps %1000 == 0:
            #        fname = "/tmp/videos/frame"+str(steps)+".mp4"
            #        skvideo.io.vwrite(fname, np.array(frames))
            #        del frames
            #        frames = []

        #frame = env.render(mode='rgb_array')
        #frames.append(frame)
        #if steps >= training_thr and steps %1000 == 0:
        #    fname = "/tmp/videos/frame"+str(steps)+".mp4"
        #    skvideo.io.vwrite(fname, np.array(frames))
        #    del frames
        #    frames = []

        if steps >= training_thr:
            print("Local Iterations: ", local_iterations)
        steps += 1

        if steps >= training_thr and steps % num_steps ==0:
            # re-train a model
            print("Training model.")
            modelTrained = True
            model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 20, batch_size=128, workers=100, use_multiprocessing=True, validation_split=0.2)
            
            # Start with new training data
            # X_train, y_train = [],[]

        if steps %2 == 0 and steps >= training_thr:
            print("At step ", steps)
            print("reward: ", prev_reward)
            print("total rewards ", total_reward)

    print("Total successes are: ", len(successful_steps))
    print("Total crashes: ", unsuccessful_landing)

