## UltraChip's e-Triops Virtual Pet
## v. 0.1
##
## e-Triops is a virtual pet in the style of a 
## classic Tamagotchi toy, meant to simulate the
## raising of a Triops.

from pynput import keyboard
import os
import time
import random
import json

global gamestate

# Interaction Handler: Parses key presses from the user
def interact(key):
    if key.char == 'f':  # Feed the triops
        n = int(input("How much food do you want to give? "))
        gamestate[foodInTank] += n
        print("Fed " + n + " pellets")
    if key.char == 'c':  # Clean the tank
        gamestate[ammonia] = 0
        gamestate[foodInTank] = 0
        print("Tank cleaned!")
    if key.char == 'r':  # Reset the game
        yn = input("Are you sure you want to ERASE " + gamestate[name] + " and completely start over? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            resetgame()
    if key.char == 'q':  # Write game to file, then quit
        yn = input("Are you sure you want to quit the game? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            savegame()
            return False
    sleep(1)
    gamestate[tod] += 1
    return True

# Reading, writing, and initializing the game state
def loadgame():
    if path.exists('etriops.sav'):
        with open('etriops.sav', 'r') as f:
            gamestate = json.loads(f.read())
    else:
        resetgame()

def savegame():
    with open('etriops.sav', 'w+') as f:
        file.write(json.dumps(gamestate))
        print("Saved game!")

def resetgame():
    gamestate = {'name': 'unnamed', 'age': 0, 'tod': 0, 'hcap': 100, 'health': 100, 'hunger': 100, 'ammonia': 0, 'foodInTank': 0}
    gamestate[name] = input("What is your tirops' name? ")
    