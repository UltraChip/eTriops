## UltraChip's e-Triops Virtual Pet
##
## e-Triops is a virtual pet in the style of a 
## classic Tamagotchi toy, meant to simulate the
## raising of a Triops.
version = "v.1.0r"

import tkinter as tk
from tkinter import simpledialog as sd
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
aniMode = "idle"

# Interaction Handler: Parses key presses from the user
def interact(key):
    if key.char == 'f':  # Feed the triops
        feed()
    if key.char == 'c':  # Clean the tank
        clean()
    if key.char == 'r':  # Reset the game
        resetprompt()
    if key.char == 'q':  # Write game to file, then quit
        closeprompt()

#    if key.char == 'P':  # Dump debugging information to console + log
#        debugDump()
#    if key.char == 'O':  # CHEAT - Force egg laying
#        logging.info("Egg-laying cheat used!")
#        eggs()
#    if key.char == 'I':  # CHEAT - Force molting
#        logging.info("Force-molt cheat used!")
#        molt()

def debugDump():
    logging.debug(gs)
    logging.debug("Game version: " + version)
    logging.debug("descAge:      " + descAge)
    logging.debug("descHealth:   " + descHealth)
    logging.debug("descHunger:   " + descHunger)
    logging.debug("descAmm:      " + descAmm)
    logging.debug("simStop:      " + str(simStop))
    logging.debug("simLock:      " + str(simLock))
    logging.debug("aniMode:      " + aniMode)

# Reading, writing, and initializing the game state
def loadgame():
    global gs
    sfn = buildfilepath("etriops.sav")
    if os.path.exists(sfn):
        with open(sfn, 'r') as f:
            gs = json.loads(f.read())
        nameDesc.config(text=gs["name"])
    else:
        initgame()

def savegame():
    with open(buildfilepath("etriops.sav"), 'w+') as f:
        f.write(json.dumps(gs))

def resetprompt():
    prompt = tk.messagebox.askquestion("Confirm Reset", "Are you sure you want to ERASE " + gs["name"] + " and completely start over?")
    if prompt == 'yes':
        initgame()

def initgame():
    global gs
    global simLock
    global aniMode
    simLock = True
    name = sd.askstring("Enter Name", "What is your triops' name?")
    gs = {'name': 'unnamed', 'age': 0, 'tod': 0, 'hcap': 100, 'health': 100, 'hunger': 100, 'ammonia': 0, 'foodInTank': 0, 'eggs': 0}
    gs["name"] = name
    nameDesc.config(text=gs["name"])
    savegame()
    simLock = False
    aniMode = "idle"
    logging.info("New hatchling " + gs["name"] + " has been born. Congratulations!")

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
      
def molt():
    global gs
    global aniMode

    aniMode = "molt"
    av = gs["age"]
    if av > 93:
        av = 93
    baseDamage = round(random.uniform(1,10), 5)
    gs["health"] = gs["health"] - (baseDamage + av)
    logging.info("Molted! Health knocked down to " + str(gs["health"]))

def eggs():
    global gs
    global aniMode

    if gs["health"] > 20:
        aniMode = "eggs"
        numeggs = random.randint(10,30)
        if gs["health"] <= 40:
            numeggs = numeggs / 2
        gs["eggs"] += numeggs
        logging.info("Laid " + str(numeggs) + " eggs!")

def death():
    def reset():
        dbox.destroy()
        initgame()

    def close():
        dbox.destroy()
        closegame()

    dbox = tk.Toplevel(gui)
    dbox.title("RIP")

    header = tk.Label(dbox, text="Unfortunately, " + gs["name"] + " has passed away.", padx=10)
    header.grid(row=0, column=0, columnspan=2)
    blankspace = tk.Label(dbox, text="   ", pady = 1)
    blankspace.grid(row=1, column=0)
    finalAge = tk.Label(dbox, text="Final Age: " + str(gs["age"]) + " days - " + descAge, width=25, anchor='w')
    finalAge.grid(row=2, column=0, columnspan=2)
    finalEggs = tk.Label(dbox, text="Total Egg Count: " + str(gs["eggs"]) + " eggs", width=25, anchor='w')
    finalEggs.grid(row=3, column=0, columnspan=2)
    dResetBtn = tk.Button(dbox, text="Reset Game", command=reset)
    dResetBtn.grid(row=4, column=0)
    dQuitBtn = tk.Button(dbox, text="Quit Game", command=close)
    dQuitBtn.grid(row=4, column=1)
    global simLock
    global aniMode
    simLock = True
    aniMode = "death"
    savegame()

def feed():
    global gs
    global aniMode

    n = sd.askinteger("Feed Triops", "How many pellets do you want to give " + gs["name"] + "?")
    if n is None:
        n = 0
    
    aniMode = "feed"
    gs["foodInTank"] += n
    logging.info(str(gs["foodInTank"]) + " pellets put in the tank.")

def clean():
    global gs
    global aniMode

    aniMode = "clean"
    gs["ammonia"] = gs["ammonia"]/4
    gs["foodInTank"] = 0
    logging.info("Cleaned tank. Ammonia now at " + str(gs["ammonia"]))

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
            time.sleep(1)
        time.sleep(0.1)

def refreshScreen():
    yellow = "#e39000"
    red = "#ff0000"
    black = "#000000"
    green = "#28bf0d"

    buildDescriptions()
    ageDesc.config(text=descAge)
    healthDesc.config(text=descHealth)
    if descHealth == "Moderate":
        healthDesc.config(fg=yellow)
    elif descHealth == "Poor" or descHealth == "CRITICAL":
        healthDesc.config(fg=red)
    else:
        healthDesc.config(fg=black)
    hungerDesc.config(text=descHunger)
    if descHunger == "Hungry":
        hungerDesc.config(fg=yellow)
    elif descHunger == "Famished" or descHunger == "STARVING":
        hungerDesc.config(fg=red)
    else:
        hungerDesc.config(fg=black)
    ammDesc.config(text=descAmm)
    if descAmm == "Dirty":
        ammDesc.config(fg=yellow)
    elif descAmm == "Toxic" or descAmm == "SEVERE TOXICITY":
        ammDesc.config(fg=red)
    else:
        ammDesc.config(fg=black)
    foodDesc.config(text=gs["foodInTank"])
    gui.after(100, refreshScreen)

def closeprompt():
    prompt = tk.messagebox.askquestion("Confirm Quit", "Are you sure you want to close the game?")
    if prompt == 'yes':
        closegame()

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
    aniThread.join()
    logging.info("aniThread has stopped.")
    sys.exit()

def idleAnimate():
    global aniFrame

    if descAge == "SnS":
        return

    framenum = gs["tod"] % 10

    if descAge == "Hatchling":
        prefix = "hatchling-"
    elif descAge == "Juvenile":
        prefix = "juvenile-"
    else:
        prefix = "adult-"

    filename = "assets/idle/" + prefix + str(framenum) + ".gif"
    aniFrame = tk.PhotoImage(file=filename)
    imagePanel.config(image=aniFrame)

def aniLoop():
    global aniFrame
    global simLock
    global aniMode

    while not simStop:
        if aniMode == "idle":
            idleAnimate()
            time.sleep(1)
        else:
            framenum = 0

            while framenum <= 7:
                if aniMode == "idle" or simStop == True:  # In certain situations the program may accidentally enter this loop when
                    break                                 # animation mode is set to idle. This conditional catches that and corrects it.
                filename = "assets/" + aniMode + "/" + str(framenum) + ".gif"
                aniFrame = tk.PhotoImage(file=filename)
                imagePanel.config(image=aniFrame)
                time.sleep(1)
                framenum += 1
            if aniMode == "death":
                aniMode = "death"
            else:
                aniMode = "idle"


# MAIN
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(buildfilepath("etriops.log")),
        logging.StreamHandler()
    ]
)

# Initialize GUI Window
lWidth = 11

gui = tk.Tk()
gui.title("eTriops  " + version)
favicon = tk.PhotoImage(file='assets/favicon.gif')
gui.iconphoto(True, favicon)
gui.resizable(width=False, height=False)
gui.bind("<Key>", interact)
gui.protocol("WM_DELETE_WINDOW", closegame)

aniFrame = tk.PhotoImage(file='assets/placeholder.gif')
imagePanel = tk.Label(gui, image=aniFrame, bg="#4c6955", borderwidth=10, relief="sunken", anchor="s")
imagePanel.grid(row=0, column=0, columnspan=4, pady=5)

nameDesc = tk.Label(gui, text = "UNNAMED", width=20, anchor="n", font=("Helvetica", 14, "bold"))
nameDesc.grid(row=1, column=0, columnspan=4)
ageDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="n", font=("Helvetica", 12, "bold"))
ageDesc.grid(row=2, column=0, columnspan=4)

healthLabel = tk.Label(gui, text="Health:", width=lWidth, anchor="w", font=("Helvetica", 10, "bold"))
healthLabel.grid(row=3, column=0)
healthDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
healthDesc.grid(row=3, column=1)
hungerLabel = tk.Label(gui, text="Hunger:", width=lWidth, anchor="w", font=("Helvetica", 10, "bold"))
hungerLabel.grid(row=3, column=2)
hungerDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
hungerDesc.grid(row=3, column=3)

ammLabel = tk.Label(gui, text="Water Quality:", width=lWidth, anchor="w", font=("Helvetica", 10, "bold"))
ammLabel.grid(row=4, column=0)
ammDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
ammDesc.grid(row=4, column=1)
foodLabel = tk.Label(gui, text="Food in Tank:", width=lWidth, anchor="w", font=("Helvetica", 10, "bold"))
foodLabel.grid(row=4, column=2)
foodDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
foodDesc.grid(row=4, column=3)

feedBtn = tk.Button(gui, text="Feed", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"), command=feed)
feedBtn.grid(row=5, column=0, padx=5, pady=5)
cleanBtn = tk.Button(gui, text="Clean", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"), command=clean)
cleanBtn.grid(row=5, column=1, padx=5, pady=5)
resetBtn = tk.Button(gui, text="Reset", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"), command=resetprompt)
resetBtn.grid(row=5, column=2, padx=5, pady=5)
quitBtn = tk.Button(gui, text="Quit", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"), command=closeprompt)
quitBtn.grid(row=5, column=3, padx=5, pady=5)

# Getting ready for core loops
bgSimThread = threading.Thread(target=bgSimLoop, daemon=True)
aniThread = threading.Thread(target=aniLoop, daemon=True)
loadgame()

# Initialize core loops and threads
bgSimThread.start()
aniThread.start()
refreshScreen()
gui.mainloop()
