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
from collections import deque
from keras.activations import relu, linear
from keras.losses import mean_squared_error
from keras.optimizers import Adam
import random


class DQN:
    def __init__(self, env):

        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space
        self.counter = 0

        #######################
        # Change these parameters to improve performance
        self.density_first_layer = 16
        self.density_second_layer = 8
        self.num_epochs = 1
        self.batch_size = 64
        self.epsilon_min = 0.01

        # epsilon will randomly choose the next action as either
        # a random action, or the highest scoring predicted action
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.gamma = 0.99

        # Learning rate
        self.lr = 0.001

        #######################

        self.rewards_list = []

        self.replay_memory_buffer = deque(maxlen=500000)
        self.num_action_space = self.action_space.n
        self.num_observation_space = env.observation_space.shape[0]


        self.model = self.initialize_model()

    def initialize_model(self):
        model = Sequential()
        model.add(Dense(self.density_first_layer, input_dim=self.num_observation_space, activation=relu))
        model.add(Dense(self.density_second_layer, activation=relu))
        model.add(Dense(self.num_action_space, activation=linear))

        # Compile the model
        model.compile(loss=mean_squared_error,optimizer=Adam(lr=self.lr))
        print(model.summary())
        return model

    def get_action(self, state):

        # The epsilon parameter decides whether we are using the 
        # Q-function to determine our next action 
        # or take a random sample of the action space. 
        if np.random.rand() < self.epsilon:
            return random.randrange(self.num_action_space)

        # Get a list of predictions based on the current state
        predicted_actions = self.model.predict(state)

        # Return the maximum-reward action
        return np.argmax(predicted_actions[0])

    def add_to_replay_memory(self, state, action, reward, next_state, done):
        self.replay_memory_buffer.append((state, action, reward, next_state, done))

    def learn_and_update_weights_by_reply(self):

        # replay_memory_buffer size check
        # if we have fewer than 64 actions in the buffer, 
        # or the counter is not 0, return
        if len(self.replay_memory_buffer) < self.batch_size or self.counter != 0:
            return

        # Early Stopping
        if np.mean(self.rewards_list[-10:]) > 180:
            return

        # Choose batch of random samples from the replay stack 
        random_sample = self.get_random_sample_from_replay_mem()

        # Get the values (in numpy array form) from the random batch of samples
        states, actions, rewards, next_states, done_list = self.get_attribues_from_sample(random_sample)

        # Use the Keras "predict_on_batch" feature to predict the targets
        # based on the random batch of next states in our replay stack
        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (1 - done_list)
        
        # Run a prediction on the states in our random sample
        target_vec = self.model.predict_on_batch(states)

        # Create a numpy array sized to match the batch_size
        indexes = np.array([i for i in range(self.batch_size)])

        # The target vector is an array of 
        # state predictions 
        target_vec[[indexes], [actions]] = targets

        # build a model with the existing states and target scores in batches of 64
        self.model.fit(states, target_vec, epochs=self.num_epochs, verbose=0)

    def get_attribues_from_sample(self, random_sample):
        states = np.array([i[0] for i in random_sample])
        actions = np.array([i[1] for i in random_sample])
        rewards = np.array([i[2] for i in random_sample])
        next_states = np.array([i[3] for i in random_sample])
        done_list = np.array([i[4] for i in random_sample])
        states = np.squeeze(states)
        next_states = np.squeeze(next_states)
        return np.squeeze(states), actions, rewards, next_states, done_list

    # Get a batch_size sample of previous iterations
    def get_random_sample_from_replay_mem(self):
        random_sample = random.sample(self.replay_memory_buffer, self.batch_size)
        return random_sample

    # Run the keras predict using the current state as input.
    # This will choose the next step.
    def predict(self, current_state):
        return self.model.predict(current_state)

    def train(self, num_episodes=2000, can_stop=True):

        frames = []

        for episode in range(num_episodes):

            # state is a vector of 8 values:
            # x and y position
            # x and y velocity
            # lander angle and angular velocity
            # boolean for left leg contact with ground
            # boolean for right leg contact with ground
            state = env.reset()
            reward_for_episode = 0
            done = False
            state = np.reshape(state, [1, self.num_observation_space])
            while not done:
                frame = env.render(mode='rgb_array')

                if episode % 10 == 0:
                    frames.append(frame)                    


                # use epsilon decay to choose the next state
                received_action = self.get_action(state)
                next_state, reward, done, info = env.step(received_action)

                # Reshape the next_state array to match the size of the observation space
                next_state = np.reshape(next_state, [1, self.num_observation_space])

                # Store the experience in replay memory
                self.add_to_replay_memory(state, received_action, reward, next_state, done)

                # add up rewards
                reward_for_episode += reward
                state = next_state
                self.update_counter()

                # update the model
                self.learn_and_update_weights_by_reply()

                #if done:
                #    break
            self.rewards_list.append(reward_for_episode)

            # Create a video from every 10th episode
            if episode % 10 == 0:
                fname = "/tmp/videos/episode"+str(episode)+".mp4"
                skvideo.io.vwrite(fname, np.array(frames))
                del frames
                frames = []

            # Decay the epsilon after each experience completion
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            # Check for breaking condition
            last_rewards_mean = np.mean(self.rewards_list[-100:])

            # Once the mean average of rewards is over 200, we can stop training
            if last_rewards_mean > 200 and can_stop:
                print("DQN Training Complete...")
                break
            print(episode, "\t: Episode || Reward: ",reward_for_episode, "\t|| Average Reward: ",last_rewards_mean, "\t epsilon: ", self.epsilon )

    def update_counter(self):
        self.counter += 1
        step_size = 5
        self.counter = self.counter % step_size

    def save(self, name):
        self.model.save(name)


if __name__=="__main__":
    rewards_list = []

    # Run 100 episodes to generate the initial training data
    num_test_episode = 100

    env = gym.make("LunarLander-v2")

    # set the numpy random number generatorseeds
    env.seed(21)
    np.random.seed(21)

    # max number of training episodes
    training_episodes = 2000
 
    # initialize the Deep-Q Network model
    model = DQN(env)

    # Train the model
    model.train(training_episodes, True)

    print("Starting Testing of the trained model...")

    done = False
    frames = []

    # Run some test episodes to see how well our model performs
    for test_episode in range(num_test_episode):
        current_state = env.reset()
        num_observation_space = env.observation_space.shape[0]
        current_state = np.reshape(current_state, [1, num_observation_space])
        reward_for_episode = 0
        done = False
        while not done:

            frame = env.render(mode='rgb_array')
            frames.append(frame)

            selected_action = np.argmax(model.predict(current_state)[0])
            new_state, reward, done, info = env.step(selected_action)
            new_state = np.reshape(new_state, [1, num_observation_space])
            current_state = new_state
            reward_for_episode += reward
        rewards_list.append(reward_for_episode)
        print(test_episode, "\t: Episode || Reward: ", reward_for_episode)
        if test_episode % 10 == 0:
            fname = "/tmp/videos/testing_run"+str(test_episode)+".mp4"
            skvideo.io.vwrite(fname, np.array(frames))
            del frames
            frames = []

    rewards_mean = np.mean(rewards_list[-100:])
    print("Average Reward: ", rewards_mean )

    
