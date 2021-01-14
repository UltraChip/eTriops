import tkinter as tk
from PIL import Image, ImageTk

gui = tk.Tk()
gui.title("eTriops")

triopCon = tk.Label(gui, text = "TRIOPS CONDITION:", width=18, anchor="w")
triopCon.grid(row=0, column=0)

nameLabel = tk.Label(gui, text="Name:", width=18, anchor="w")
nameLabel.grid(row=1, column=0)
nameDesc = tk.Label(gui, text="SnS", width=9, anchor="w")
nameDesc.grid(row=1, column=1)
frameImg = Image.open("assets/placeholder.gif")
frameImg = frameImg.resize(100, 100)
aniFrame = ImageTk.PhotoImage(frameImg)
aniFrame = tk.Label(gui, image=frameImg)
aniFrame.grid(row=1, column=2)


gui.mainloop()