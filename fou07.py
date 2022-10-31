from tkinter import Tk

from Gui import Gui
from Pilote import Pilote
import time
from Websocket import Websocket

pilote = Pilote()

root = Tk()
gui = Gui(root)
gui.setPilote(pilote)

ws = Websocket()
ws.start()

while(1):
    pilote.majSerie()
    gui.majCanvas()
    root.update()
    if(ws.connected) :
        ws.setEnvoi(pilote.xPos,pilote.yPos)
