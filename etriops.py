## UltraChip's e-Triops Virtual Pet
## v. 0.1
##
## e-Triops is a virtual pet in the style of a 
## classic Tamagotchi toy, meant to simulate the
## raising of a Triops.

from pynput import keyboard
import time

# Interaction Handler: Parses key presses from the user
def interact(key):
    if key.char == 'f':
        # Feed Triops
    if key.char == 'c':
        # Clean Tank
    if key.char == 'r':
        # Reset Triops
    if key.char == 'q':
        # Quit Game
        # Write game state to file
        return False
    sleep(1)
    return True

# Initialize the game
def startgame():
    