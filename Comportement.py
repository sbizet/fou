import numpy as np
from Utils import *
class Comportement():
    def __init__(self):
        self.id = 0  # doit être choisi par l'utilisateur
        self.newId = True
        self.vX = 0
        self.vY = 0
        self.heightFou = 0
        self.widthFou = 0
        self.xPos = 0
        self.yPos = 0
        self.resolution = 10
        self.indexPause = 0
        self.enPause = False
        self.dureePause = 0
        self.vMinArduino = 25 # en dessous de 25 pas/s on considère une vitesse nulle
        self.vMaxArduino = 2000

        self.carre = None
        self.cercle = None

    def maj(self):
        if(self.enPause):
            self.compteurPause(self.dureePause)
        else :
            if(self.id==0):
                if(self.newId) :
                    self.vX = 0
                    self.vY = 0
            if(self.id==1):
                if(self.newId) :
                    self.carre = Carre(self.resolution) # première occurence, on créé l'instance carré
                    self.carre.setParam(800,500,1000) # accel,vitesse,taille
                vX,vY,self.dureePause = self.carre.maj(self.vX,self.vY,self.xPos,self.yPos) # maj du comportement carré, avec renseignement sur la vitesse et la position en cours
                self.vX,self.vY = self.miseEnForme(vX,vY)
            if(self.id == 2):
                if(self.newId) :
                    self.cercle = Cercle(self.resolution) # première occurence, on créé l'instance carré
                    self.cercle.setParam(400,1000,0) # vitesse,taille,angle origine
                vX,vY,self.dureePause = self.cercle.maj() # maj du comportement carré, avec renseignement sur la vitesse et la position en cours
                self.vX,self.vY = self.miseEnForme(vX,vY)

            if (self.dureePause>0) :
                self.enPause = True

            self.newId = False

    def setId(self,_id):
        if(self.id != id) :
            self.newId = True
        else :
            self.newId = False
        self.id = _id

    def miseEnForme(self,vX,vY):
        if(abs(vX)<self.vMinArduino) :
            vX = 0
        if(abs(vX)>self.vMaxArduino) :
            vX = self.vMaxArduino

        if(abs(vY)<self.vMinArduino) :
            vY = 0
        if(abs(vY)>self.vMaxArduino) :
            vY = self.vMaxArduino
        return vX,vY

    def miseEnPause(self,dureePause):
        self.vX = 0
        self.vY = 0
        self.enPause = True
        self.dureePause = dureePause

    def compteurPause(self,dureePause):
        if (self.indexPause == dureePause) :
            self.indexPause = 0
            self.enPause = False
        else :
            self.indexPause += 1

class Cercle():
    def __init__(self,res):
        self.taille = 1000
        self.vMax = 500
        self.angle = 0

    def setParam(self,vMax,taille,angleOrigine):
        self.dAngle = 0.0228*vMax/taille # très approximatif ...
        self.vMax = vMax
        self.angle = angleOrigine

    def maj(self):
        self.angle += self.dAngle
        vX = self.vMax * np.cos(self.angle)
        vY = self.vMax * np.sin(self.angle)
        return vX,vY,0

class Carre():
    def __init__(self,res):
        self.phase = -1
        self.taille = 1000
        self.aMax = 1000
        self.vMax = 500
        self.goto = Goto(res)

    def setParam(self,aMax,vMax,taille):
        self.taille = taille
        self.aMax = aMax
        self.vMax = vMax

    def maj(self,vX_old,vY_old,xPos,yPos):
        dureePause = 0
        if(self.phase == -1):
            self.goto.setParam(self.aMax,self.vMax,self.taille+xPos,yPos)
            self.phase = 0
            print("Carré Phase = " + str(self.phase))
        if(self.phase == 0):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos,self.taille+yPos)
                self.phase = 1
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 1):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos-self.taille,yPos)
                self.phase = 2
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 2):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.goto.init()
                self.goto.setParam(self.aMax,self.vMax,xPos,yPos-self.taille)
                self.phase = 3
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 3):
            vX,vY = self.goto.maj(vX_old,vY_old,xPos,yPos)
            if(vX == 0 and vY == 0):
                self.phase = 4
                print("Carré Phase = " + str(self.phase))
        if(self.phase == 4):
            self.goto.init()
            vX = 0
            vY = 0
            dureePause = 30
            self.phase = -1
        return vX,vY,dureePause
