# DotPattern
The DotPattern game is an Otree-based social experiment where the participants are shown a series of seed patterns and asked to reproduce them from memory. In our version, a flexible network structure is embedded in the game. 

Language: Norwegian Bokmål


# Usage
## Devserver (Debug/Test)
Download the *.zip* file, go to the file then run
```sh
cd DotPattern
```

Then run the following command to start the server
```sh
otree devserver
```
Then open your browser and go to the following link http://localhost:8000/ as instructed.

## Release
For actual release, make sure the *DEBUG* variable in [the init file](DotPattern/pattern/__init__.py) is set to *False*.

# Network Construction
The source code for constructing and scheduling is contained in the [network](DotPattern/network/) folder. It does not need to be run explicitly, but you can change the following variables (with default values after =):
- random.seed(375)
- N_NEIGHBORS = 2
- N_NODES = 3
- MAX_ROUNDS = 10 

# Game Settings
The default values for the game are:
- PATTERN_SIZE = 10 (a 10x10 grid)
- N_DOTS = 12 (number of squares coloured)
- N_PARTICIPANTS = 10
- PATTERN_DISPLAY_TIME = 10 (seconds)
- REPRODUCE_TIME = 60 (seconds)
- NOODLE_TIME = 10 (the time for displaying random lines in seconds)

These values can be adjusted in [the init file](DotPattern/pattern/__init__.py). 


# Deployment

You will need a Heroku account veriyfied with a credit card to deploy the game. Create an Heroku app, then go to [Otree Hub](https://www.otreehub.com/my_projects/). Create your .otreezip file by running

```py
otree zip
```

Then upload the .otreezip file to Otree Hub by clicking the **Deploy Button**.

Then follow the instructions to run it.
