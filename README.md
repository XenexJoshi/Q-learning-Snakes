Q-Learning Snakes:

This program contains a simple implementation of the classic snakes game using pygame, and a Q-learning trainer and agent that implement a model that uses the Q-learning algorithm and Bellman equation to train the program to choose the optimal action based on its previous instances to maximize the total score during gameplay. The model uses a system of positive and
negative rewards, where the positive rewards reinforce the correct course of action like landing on food, and the negative reward penalizes the program when it performs incorrect actions like crashing into a wall or being stuck in an unproductive loop.

To run the program, clone the repository into your device, navigate to the main.py file, and run.

Required modules:

    pygame
    torch
    numpy
    matplotlib
    ipython

It is recommended to setup a Python virtual environment, and install the dependencies inside the virtual environment to make the run smoother. This can be done by following the following commands:

    python3 -m venv .venv 
    source .venv/bin/activate **mac**
    .venv\Scripts\activate **windows**
    pip install pygame torch numpy
    pip install matplotlib ipython
