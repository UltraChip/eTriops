import tkinter as tk

dummyname="Jimmy"
age=68

def interact(key):
    if key.char == 'f':
        deathbox()

def reseti():
    print("Oh Noes!")

def deathbox():
    def reset():
        dbox.destroy()
        reseti()

    def close():
        dbox.destroy()
        print("Quit")

    dbox = tk.Toplevel(gui)
    dbox.title("RIP")

    header = tk.Label(dbox, text="Unfortunately, " + dummyname + " has passed away.", padx=10)
    header.grid(row=0, column=0, columnspan=2)
    blankspace = tk.Label(dbox, text="   ", pady = 1)
    blankspace.grid(row=1, column=0)
    finalAge = tk.Label(dbox, text="Final Age: " + str(age) + " days - Middle Aged", width=25, anchor='w')
    finalAge.grid(row=2, column=0, columnspan=2)
    finalEggs = tk.Label(dbox, text="Total Egg Count: 268 eggs", width=25, anchor='w')
    finalEggs.grid(row=3, column=0, columnspan=2)
    dResetBtn = tk.Button(dbox, text="Reset Game", command=reset)
    dResetBtn.grid(row=4, column=0)
    dQuitBtn = tk.Button(dbox, text="Quit Game", command=close)
    dQuitBtn.grid(row=4, column=1)


lWidth = 13

gui = tk.Tk()
gui.title("eTriops")
favicon = tk.PhotoImage(file='assets/favicon.gif')
gui.iconphoto(True, favicon)
gui.bind("<Key>", interact)

aniFrame = tk.PhotoImage(file='assets/placeholder.gif')
imagePanel = tk.Label(gui, image=aniFrame, anchor="n")
imagePanel.grid(row=0, column=0, columnspan=4)

nameDesc = tk.Label(gui, text = "UNNAMED", width=lWidth, anchor="n")
nameDesc.grid(row=1, column=0, columnspan=4)
ageDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="n")
ageDesc.grid(row=2, column=0, columnspan=4)

healthLabel = tk.Label(gui, text="Health:", width=lWidth, anchor="w")
healthLabel.grid(row=3, column=0)
healthDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
healthDesc.grid(row=3, column=1)
hungerLabel = tk.Label(gui, text="Hunger:", width=lWidth, anchor="w")
hungerLabel.grid(row=3, column=2)
hungerDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
hungerDesc.grid(row=3, column=3)

ammLabel = tk.Label(gui, text="Ammonia:", width=lWidth, anchor="w")
ammLabel.grid(row=4, column=0)
ammDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
ammDesc.grid(row=4, column=1)
foodLabel = tk.Label(gui, text="Food in Tank:", width=lWidth, anchor="w")
foodLabel.grid(row=4, column=2)
foodDesc = tk.Label(gui, text="SnS", width=lWidth, anchor="w")
foodDesc.grid(row=4, column=3)

feedBtn = tk.Button(gui, text="Feed", width=lWidth, anchor="n", command=deathbox)
feedBtn.grid(row=5, column=0)
cleanBtn = tk.Button(gui, text="Clean", width=lWidth, anchor="n")
cleanBtn.grid(row=5, column=1)
resetBtn = tk.Button(gui, text="Reset", width=lWidth, anchor="n")
resetBtn.grid(row=5, column=2)
quitBtn = tk.Button(gui, text="Quit", width=lWidth, anchor="n")
quitBtn.grid(row=5, column=3)

gui.mainloop()
#print("Goodbye!")