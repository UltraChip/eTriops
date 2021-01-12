## UltraChip's e-Triops Virtual Pet
## v. 0.1
##
## e-Triops is a virtual pet in the style of a 
## classic Tamagotchi toy, meant to simulate the
## raising of a Triops.

from pynput import keyboard
from clear_screen import clear
import time
import random
import json
import sys

global gs
global mbuffer

# Interaction Handler: Parses key presses from the user
def interact(key):
    if key.char == 'f':  # Feed the triops
        n = int(input("How much food do you want to give? "))
        gs[foodInTank] += n
        mbuffer.append(str("Fed " + n + " pellets!"))
    if key.char == 'c':  # Clean the tank
        gs[ammonia] = gs[ammonia] / 4
        gs[foodInTank] = 0
        mbuffer.append("Tank cleaned!")
    if key.char == 'r':  # Reset the game
        yn = input("Are you sure you want to ERASE " + gs[name] + " and completely start over? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            resetgame()
    if key.char == 'q':  # Write game to file, then quit
        yn = input("Are you sure you want to quit the game? (Y/N) ")
        if yn.upper() == 'Y' or yn.upper() == 'YES':
            savegame()
            sys.exit()
    return True

# Reading, writing, and initializing the game state
def loadgame():
    if path.exists('etriops.sav'):
        with open('etriops.sav', 'r') as f:
            gs = json.loads(f.read())
    else:
        resetgame()

def savegame():
    with open('etriops.sav', 'w+') as f:
        file.write(json.dumps(gs))
        mbuffer.append("Saved game!")

def resetgame():
    gs = {'name': 'unnamed', 'age': 0, 'tod': 0, 'hcap': 100, 'health': 100, 'hunger': 100, 'ammonia': 0, 'foodInTank': 0, 'eggs': 0}
    gs[name] = input("What is your triops' name? ")
    savegame()

# Update the game's state after a clock tick
def tick():
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

    if random.randint(1,259200) == 3:  # 1 in 259,200 chance of molting per tick should result in an average molt rate of
        molt()                         # once every three days or so.
    
    if random.randint(1,259200) == 6 and gs[age] >= 14:  # Once a triop reaches day 14 or older it has a random chance of
        eggs()                                           # laying eggs (average once every three days).

    if gs[tod] % 1800 == 0:  # Save the game every 30 minutes (1,800 seconds = 30 minutes)
        savegame()

    # Dying and enforcing the health cap
    if gs[health] > gs[hcap]:
        gs[health] = gs[hcap]
    if gs[health] <= 0:
        death()
    
def molt():
    av = gs[age]
    if av > 93:
        av = 93
    gs[health] = gs[health] - (random.randint(1,10) + av)
    mbuffer.append("Molted!")

def eggs():
    if gs[health] > 20:
        numeggs = random.randint(10,30)
        if gs[health] <= 40:
            numeggs = numeggs / 2
        gs[eggs] += numeggs
        mbuffer.append(str(gs[name] + " just laid " + numeggs + " eggs!"))

def death():
    stage = ""
    if gs[age] < 3:
        stage = "Hatchling"
    if gs[age] >= 3 and gs[age] < 10:
        stage = "Juvenile"
    if gs[age] >= 10 and gs[age] < 14:
        stage = "Young Adult"
    if gs[age] >= 14 and gs[age] < 30:
        stage = "Adult"
    if gs[age] >= 30 and gs[age] < 60:
        stage = "Middle Aged"
    if gs[age] >= 60 and gs[age] < 80:
        stage = "Senior"
    if gs[age] >= 80 and gs[age] < 90:
        stage = "Elder"
    if gs[age] >= 90:
        stage = "LEGENDARY"

    clear()
    print ("")
    print ("Unfortunately, " + gs[name] + " has passed away.")
    print ("")
    print ("Final age:       " + gs[age] + " days - " + stage)
    print ("Total egg count: " + gs[eggs] + " eggs")
    print ("")
    yn = input("Would you like to reset the game and start over? (Y/N) ")
    if yn.upper() == 'Y' or yn.upper() == 'YES':
        resetgame()
    else:
        sys.exit()

# Report on the game's current status - usually run after processing a tick
def report():
    stage = ""
    if gs[age] < 3:
        stage = "Hatchling"
    if gs[age] >= 3 and gs[age] < 10:
        stage = "Juvenile"
    if gs[age] >= 10 and gs[age] < 14:
        stage = "Young Adult"
    if gs[age] >= 14 and gs[age] < 30:
        stage = "Adult"
    if gs[age] >= 30 and gs[age] < 60:
        stage = "Middle Aged"
    if gs[age] >= 60 and gs[age] < 80:
        stage = "Senior"
    if gs[age] >= 80 and gs[age] < 90:
        stage = "Elder"
    if gs[age] >= 90:
        stage = "LEGENDARY"
    
    hcon = ""
    if gs[health] < 20:
        hcon = "CRIICAL"
    if gs[health] >=20 and gs[health] < 50:
        hcon = "Poor"
    if gs[health] >= 50 and gs[health] < 80:
        hcon = "Moderate"
    if gs[health] >= 80 and gs[health] < 90:
        hcon = "Good"
    if gs[health] >= 90 and gs[health] < 95:
        hcon = "Excellent"
    if gs[health] >= 95:
        hcon = "Peak Condition"
    
    amcon = ""
    if gs[ammonia] < 7:
        amcon = "Excellent"
    if gs[ammonia] >= 7 and gs[ammonia] < 50:
        amcon = "Fair"
    if gs[ammonia] >= 50 and gs[ammonia] < 100:
        amcon = "Dirty"
    if gs[ammonia] >= 100 and gs[ammonia] < 158:
        amcon = "Toxic"
    if gs[ammonia] >= 158:
        amcon = "SEVERE TOXICITY"

    clear()
    print ("")
    print ("TRIOPS CONDITION:")
    print ("Name:   " + gs[name])
    print ("Age:    " + gs[age] + " days - " + stage)
    print ("Health: " + gs[health] + " HP - " + hcon)
    print ("")
    print ("TANK CONDITION:")
    print ("Ammonia:      " + gs[ammonia] + " - " + amcon)
    print ("Food in tank: " + gs[foodInTank] + " pellets")
    print ("")
    print ("")
    print ("(F)eed, (C)lean Tank, (R)eset game, or (Q)uit")

# Main
loadgame()

with keyboard.Listener(on_press=interact) as listener:
    while listener.running:
        tick()
        report()
        sleep(1)
