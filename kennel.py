## UltraChip's e-Triops Virtual Pet
## -= KENNEL =-
##
## e-Triops is a virtual pet in the style of a 
## classic Tamagotchi toy, meant to simulate the
## raising of a Triops.
##
## The "Kennel" is an experimental program that
## allows an eTriops to live unattended for a 
## short period, with automatic feedings. 
## No GUI available. Use at own risk!

version = "v.1.0e - KENNEL"

import time
import random
import json
import os
import sys
import threading
import logging

# Global Vars
gs = {}
descAge = "SnS"
descHealth = "SnS"
descHunger = "SnS"
descAmm = "SnS"
simStop = False
simLock = False
feederDose = 1
feederRate = 86400

def reportStatus():
    os.system("clear")
    print(gs["name"] + " - " + descAge)
    print("")
    print("Health:        " + descHealth)
    print("Hunger:        " + descHunger)
    print("Water Quality: " + descAmm)
    print("Food in Tank:  " + str(gs["foodInTank"]))

# Reading, writing, and initializing the game state
def loadgame():
    global gs
    sfn = buildfilepath("etriops.sav")
    if os.path.exists(sfn):
        with open(sfn, 'r') as f:
            gs = json.loads(f.read())
        logging.info(gs["name"] + " has been succesfully loaded in to the kennel!")
        buildDescriptions()
        reportStatus()
    else:
        logging.info(sfn + " not found! Exiting...")
        sys.exit()

def savegame():
    with open(buildfilepath("etriops.sav"), 'w+') as f:
        f.write(json.dumps(gs))

def buildfilepath(filename):
    homedir = os.path.expanduser("~")
    return homedir + "/" + filename

# Update the game's state after a clock tick
def tick():
    global gs

    gs["tod"] += 1
    gs["health"] += 0.08333   # Gain 0.08333 health per tick (roughly enough to restore 50HP over 10 minutes)
    gs["hunger"] += -0.00092  # Lose 0.00092 hunger per tick (roughly enough to be ~20 hunger after 24 hours)
    gs["ammonia"] += 0.00008  # Gain 0.00008 ammonia per tick (enough for 100% toxicity after a little more than 14 days)
    gs["hcap"] = 100-(gs["ammonia"]/2)

    # Advance the age if it's been 1 day's worth of ticks
    if gs["tod"] >= 86400:  # 86,400 - the number of seconds in a day
        gs["age"] += 1
        gs["tod"] = 0

    # Hunger and eating
    if gs["hunger"] < 95 and gs["foodInTank"] > 0:
        gs["foodInTank"] += -1
        gs["hunger"] += 20
        if gs["hunger"] > 100:
            gs["hunger"] = 100
    if gs["hunger"] <= 0:         # If starving, decrease health by 0.00462 (+ 0.08333 to counteract natural regen) per tick.
        gs["health"] += -0.08795  # Assuming the triops is otherwise healthy it will die in ~6 hours.
    if gs["age"] < 3:       # If the triops is under 3 days old it can't get hungry.
        gs["hunger"] = 100

    gs["ammonia"] += gs["foodInTank"] * 0.00004  # Add an extra half-dose of ammonia for every uneaten food pellet in the tank

    if random.randint(1,259200) == 3:  # 1 in 259,200 chance of molting per tick should result in an average molt rate of
        molt()                         # once every three days or so.
    
    if random.randint(1,259200) == 6 and gs["age"] >= 14:  # Once a triop reaches day 14 or older it has a random chance of
        eggs()                                             # laying eggs (average once every three days).

    # Dying and enforcing the health cap
    if gs["health"] > gs["hcap"]:
        gs["health"] = gs["hcap"]
    if gs["health"] <= 0:
        death()

    if gs["tod"] % 1800 == 0:  # Save the game every 30 minutes (1,800 seconds = 30 minutes)
        savegame()
    if gs["tod"] % feederRate == 0:  # Auto-feed according to feederRate
        feed()
      
def molt():
    global gs

    av = gs["age"]
    if av > 93:
        av = 93
    baseDamage = round(random.uniform(1,10), 5)
    gs["health"] = gs["health"] - (baseDamage + av)
    logging.info("Molted! Health knocked down to " + str(gs["health"]))

def eggs():
    global gs

    if gs["health"] > 20:
        numeggs = random.randint(10,30)
        if gs["health"] <= 40:
            numeggs = numeggs / 2
        gs["eggs"] += numeggs
        logging.info("Laid " + str(numeggs) + " eggs!")

def death():
    print("Unfortunately, " + gs["name"] + " has passed away.")
    print("Final Age: " + str(gs["age"]) + " days - " + descAge)
    print("Total Egg Count: " + str(gs["eggs"]) + " eggs")
    print("")
    closegame()

def feed():
    global gs
    global feederDose
    gs["foodInTank"] += feederDose
    logging.info(str(feederDose) + " pellets put in the tank.")

def buildDescriptions():
    global descAge
    global descHealth
    global descHunger
    global descAmm

    if gs["age"] < 3:
        descAge = "Hatchling"
    if gs["age"] >= 3 and gs["age"] < 10:
        descAge = "Juvenile"
    if gs["age"] >= 10 and gs["age"] < 14:
        descAge = "Young Adult"
    if gs["age"] >= 14 and gs["age"] < 30:
        descAge = "Adult"
    if gs["age"] >= 30 and gs["age"] < 60:
        descAge = "Middle Aged"
    if gs["age"] >= 60 and gs["age"] < 80:
        descAge = "Senior"
    if gs["age"] >= 80 and gs["age"] < 90:
        descAge = "Elder"
    if gs["age"] >= 90:
        descAge = "LEGENDARY"
    
    if gs["health"] < 20:
        descHealth = "CRITICAL"
    if gs["health"] >=20 and gs["health"] < 50:
        descHealth = "Poor"
    if gs["health"] >= 50 and gs["health"] < 80:
        descHealth = "Moderate"
    if gs["health"] >= 80 and gs["health"] < 90:
        descHealth = "Good"
    if gs["health"] >= 90 and gs["health"] < 95:
        descHealth = "Excellent"
    if gs["health"] >= 95:
        descHealth = "Peak Condition"
    
    if gs["hunger"] <= 0:
        descHunger = "STARVING"
    if gs["hunger"] > 0 and gs["hunger"] < 25:
        descHunger = "Famished"
    if gs["hunger"] >= 25 and gs["hunger"] < 50:
        descHunger = "Hungry"
    if gs["hunger"] >= 50 and gs["hunger"] < 75:
        descHunger = "Peckish"
    if gs["hunger"] >= 75 and gs["hunger"] < 95:
        descHunger = "Full"
    if gs["hunger"] >= 95:
        descHunger = "Stuffed"
    
    if gs["ammonia"] < 7:
        descAmm = "Excellent"
    if gs["ammonia"] >= 7 and gs["ammonia"] < 50:
        descAmm = "Fair"
    if gs["ammonia"] >= 50 and gs["ammonia"] < 100:
        descAmm = "Dirty"
    if gs["ammonia"] >= 100 and gs["ammonia"] < 158:
        descAmm = "Toxic"
    if gs["ammonia"] >= 158:
        descAmm = "SEVERE TOXICITY"

def bgSimLoop():
    while not simStop:      # Keep looping until simStop flag is True
        while not simLock:  # If simLock is True then break this loop and idle
            tick()          # until it becomes False again.
            buildDescriptions()
            reportStatus()
            time.sleep(1)
        time.sleep(0.1)

def closegame():
    global simStop
    global simLock
    simLock = True
    simStop = True
    logging.info("Shutting down eTriops...")
    savegame()
    logging.info("Saved game state.")
    logging.info("Sending kill signal to all threads...")
    bgSimThread.join()
    logging.info("bgSimThread has stopped.")
    logging.info(gs["name"] + " has left the kennel.")
    sys.exit()


# MAIN

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(buildfilepath("etriops.log")),
        logging.StreamHandler()
    ]
)

# Getting ready for core loops
bgSimThread = threading.Thread(target=bgSimLoop, daemon=True)
loadgame()

# Set up the AutoFeeder
feederDose = int(input("How many pellets per feeding? "))
feederRate = int(input("How often do you want to feed " + gs["name"] + " (in hours)? ")) * 3600

# Initialize core loops and threads
bgSimThread.start()
while True:
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        closegame()