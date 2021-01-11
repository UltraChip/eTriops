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
        report(str("Fed " + n + " pellets"))
    if key.char == 'c':  # Clean the tank
        gamestate[ammonia] = gamestate[ammonia] / 4
        gamestate[foodInTank] = 0
        report("Tank cleaned!")
    if key.char == 'r':  # Reset the game
        yn = input("Are you sure you want to ERASE " + gamestate[name] + " and completely start over? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            resetgame()
    if key.char == 'q':  # Write game to file, then quit
        yn = input("Are you sure you want to quit the game? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            savegame()
            return False
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
        report("Saved game!")

def resetgame():
    gamestate = {'name': 'unnamed', 'age': 0, 'tod': 0, 'hcap': 100, 'health': 100, 'hunger': 100, 'ammonia': 0, 'foodInTank': 0}
    gamestate[name] = input("What is your triops' name? ")
    savegame()

# Update the game's state after a clock tick
def tick(gs):
    gs[tod] += 1
    gs[health] += 0.08333   # Gain 0.08333 health per tick (roughly enough to restore 50HP over 10 minutes)
    gs[hunger] += -0.00092  # Lose 0.00092 hunger per tick (roughly enough to be ~20 hunger after 24 hours)
    gs[ammonia] += 0.00008  # Gain 0.00008 ammonia per tick (enough for 100% toxicity after a little more than 14 days)
    gs[hcap] = 100-(gs[ammonia]/2)

    # Advance the age if it's been 1 day's worth of ticks
    if gs[tod] >= 86400:  # 86,400 - the number of seconds in a day
        gs[age] += 1
        gs[tod] = 0

    # Hunger and eating
    if gs[hunger] < 99 and gs[foodInTank] > 0:
        gs[foodInTank] += -1
        gs[hunger] += 20
        if gs[hunger] > 100:
            gs[hunger] = 100
    if gs[hunger] <= 0:         # If starving, decrease health by 0.00462 (+ 0.08333 to counteract natural regen) per tick.
        gs[health] += -0.08795  # Assuming the triops is otherwise healthy it will die in ~6 hours.

    gs[ammonia] += gs[foodInTank] * 0.00008  # Add an extra dose of ammonia for every uneaten food pellet in the tank

    if gs[health] > gs[hcap]:
        gs[health] = gs[hcap]
    if gs[health] <= 0:
        death()
    

# Main
loadgame()

with keyboard.Listener(on_press=interact) as listener:
    while listener.running:
        tick(gamestate)
        report("")
        sleep(1)
