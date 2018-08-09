# Lab 4: More Reinforcement

The Reinforcement container built in the homework also includes some more simplistic examples running in 2D environments. One of these is a lunar lander simulation. Here, the lander is the agent, and the reward is attempting a safe landing between two flags denoting a landing site.

## Running the Simulation

Enable X, enter the docker container, and navigate to `/jetson-reinforcement/build/aarch64/bin`. Run the following command to start up the lunar lander simulation:
```
python gym-RL.py --env=LunarLander-v2 --render
```
After a while of loading, the following screen should pop up. The terminal will also begin displaying information for each episode run: 

<img src="https://raw.githubusercontent.com/dusty-nv/jetson-reinforcement/master/docs/images/LunarLander.png">

## Interpreting the Results

During the first few episodes, the lunar lander will hilariously crash onto the surface. However, after around 50 episodes, the lunar lander will begin attempting to land between the flags, and after a few hundred episodes will begin to land with a controled descent. Pay attention to the terminal output of each episode's performance, which should look similar to this:
```
Episode 010   Reward: -508.10   Last length: 079   Average length: 18.20
```
Note how the simulation evaluates its own performance in landing with the "Reward" value, which should naturally increase over time and reach the positive hundreds. As mentioned in the reinforcement learning definition, the agent (the lander) is attempting to run its task in a way to maximize the reward (the landing site). Each episode means more experience gathered for the landing process, of which the listed length is only a small part of. 

The lunar lander is a simple yet straightfoward way of approaching reinforcement learning, which provides an excellent view of how agents gain experience over time to maximize rewards. As for real-life application, the agent could easily be ported over to situations such as drone landings in precise locations.
