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
Installation
============

You can perform a minimal install of ``gym`` with:

    git clone https://github.com/openai/gym.git
    cd gym
    pip install -e .

Another method:

    pip install gym

You'll be able to run a few environments right away:

- algorithmic
- toy_text
- classic_control (you'll need ``pyglet`` to render though)

## Example notebook

Using the Jupyter notebook Docker image from the homework, proceed to open the attached notebook lab1.ipynb and follow along the code with the instructors help.


