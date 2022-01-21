# Description

This project is an implementation of the snake game in Python.
It was first written during the Wagon bootcamp and used as a demo during the
project presentations.

The project was to develop an AI playing the snake game. I planned to use
Reinforcement Learning to train this AI.

Reinforcement Learning is the training of machine learning models to make
a sequence of decisions. The agent learns to achieve a goal in an environment
This demo was used to demonstrate that the environment was easy to develop.
Pygame was used for the visual aspect.

This AI project had not been choosen during the Bootcamp and will probably be
done as a personal challenge soon.

# Installation

Python >=3.8.5 and pip needed. Create virtual environment with the tool of your choice
and activate it. Below are instructions to do setup a virtual environment
assuming pyenv is installed.

Install Python 3.8.5 and create a virtual environment named pysnake :

```bash
pyenv install 3.8.5
pyenv virtualenv 3.8.5 pysnake

```

Clone the project and move to the new directory :

```bash
git clone git@github.com:sebvey/pysnake.git
cd pysnake
```

Activate the virtual environment and install the package :
```bash
pyenv local pysnake
pip3 install -r requirements.txt
pip3 install .
```

# Run Pysnake

```bash
pygame-app
```
