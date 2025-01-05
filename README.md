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

Attached below is the progression plot after running the trainer for 100 iterations. The scores started to increase substantially after 80 runs, after which the program began to exploit its previous data rather than explore new strategies i.e. the program transitioned from its exploration stage to its exploitation stage. The highest score achieved during this session was 55.
<img width="625" alt="Screenshot 2025-01-04 at 6 44 10 PM" src="https://github.com/user-attachments/assets/d4ba6178-2707-4e50-a58e-f7e54d8877a1" />

