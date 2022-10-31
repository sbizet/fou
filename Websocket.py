import asyncio
import websockets
import threading
import json

class Websocket(threading.Thread) :
    def __init__(self):
        threading.Thread.__init__(self)
        self.dataEnvoi = ""
        self.connected = False

    def run(self):
        # must set a new loop for asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())
        # setup a server
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.listen, 'localhost', 8484))
        # keep thread running
        asyncio.get_event_loop().run_forever()

    def setEnvoi(self,x,y):
        dict = {"xPos" : 0,"yPos" : 0}
        dict["xPos"] = x
        dict["yPos"] = y
        self.dataEnvoi = json.dumps(dict)

    async def listen(self,websocket, path):
        print("Connection au websocket")
        self.connected = True
        while (self.connected):
            try :
                dataRecu = await websocket.recv()
                await websocket.send(self.dataEnvoi)
            except :
                self.connected = False
