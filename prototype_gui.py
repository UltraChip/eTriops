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


lWidth = 11

gui = tk.Tk()
gui.title("eTriops  v.0.5 (ALPHA)")
favicon = tk.PhotoImage(file='assets/favicon.gif')
gui.iconphoto(True, favicon)
gui.bind("<Key>", interact)

aniFrame = tk.PhotoImage(file='assets/placeholder.gif')
imagePanel = tk.Label(gui, image=aniFrame, borderwidth=10, relief="sunken", anchor="s")
imagePanel.grid(row=0, column=0, columnspan=4, pady=5)

nameDesc = tk.Label(gui, text = "UNNAMED", width=lWidth, anchor="n", font=("Helvetica", 14, "bold"))
nameDesc.grid(row=1, column=0, columnspan=4)
ageDesc = tk.Label(gui, text="Adult", width=lWidth, anchor="n", font=("Helvetica", 12, "bold"))
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

feedBtn = tk.Button(gui, text="Feed", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"), command=deathbox)
feedBtn.grid(row=5, column=0, padx=5, pady=10)
cleanBtn = tk.Button(gui, text="Clean", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"))
cleanBtn.grid(row=5, column=1, padx=5, pady=5)
resetBtn = tk.Button(gui, text="Reset", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"))
resetBtn.grid(row=5, column=2, padx=5, pady=5)
quitBtn = tk.Button(gui, text="Quit", width=lWidth, anchor="n", font=("Helvetica", 10, "bold"))
quitBtn.grid(row=5, column=3, padx=5, pady=5)

gui.mainloop()
#print("Goodbye!")