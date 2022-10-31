import numpy as np

def calcNPas(v):
    redPas = calcRedPas(v)
    if(v<0) : redPas = -redPas
    if(v==0) : redPas =0
    return redPas

def calcRedPas(v):
    v = int(abs(v))
    if (v > 550) : # FULLSTEP
        redPas = 1
    elif (v>260) : #HALF STEP
        redPas = 1/2
    elif (v>100): #QUARTER STEP
        redPas = 1/4
    elif (v>50) : #EIGHTH STEP
        redPas = 1/8
    else : #1/16 de pas
        redPas = 1/16
    return redPas

def setAmaxXY(res,aMax,vX,oldVX,vY,oldVY):
    if(vX == 0) : redPasX = calcRedPas(oldVX)
    else : redPasX = calcRedPas(vX)
    if(vY == 0) : redPasY = calcRedPas(oldVY)
    else : redPasY = calcRedPas(vY)
    if(vX==0) : aX = -oldVX*oldVX/(redPasX*res)
    else : aX = (vX - oldVX)*vX/(redPasX*res)
    if(vY==0) : aY = -oldVY*oldVY/(redPasY*res)
    else : aY = (vY - oldVY)*vY/(redPasY*res)
    a = np.sqrt(aX*aX + aY*aY)
    if(a>aMax):
        aX = aX*aMax/a
        deltaX = oldVX*oldVX + 4*aX*redPasX*res

        if(deltaX>=0):
            vv = vX
            if(vX==0):vv=oldVX
            if(vv>0) :
                vX=(oldVX + np.sqrt(deltaX))/2
            else : vX=(oldVX - np.sqrt(deltaX))/2
        else : vX = 0

        aY = aY*aMax/a
        deltaY = oldVY*oldVY + 4*aY*redPasY*res
        if(deltaY>=0):
            vv = vY
            if(vY==0):vv=oldVY
            if(vv>0) :
                vY=(oldVY + np.sqrt(deltaY))/2
            else : vY=(oldVY - np.sqrt(deltaY))/2
        else : vY = 0

    return vX,vY


class Goto():
    def __init__(self,res):
        self.resolution = res
        self.xPos0 = 0
        self.yPos0 = 0
        self.init()

    def setParam(self,aMax,vMax,xCible,yCible):
        self.aMax = aMax
        self.vMax = vMax
        self.xCible = xCible
        self.yCible = yCible

    def init(self):
        self.phase = -1
        self.dAccel = 0
        self.index=0

    def maj(self,vX_old,vY_old,xPos,yPos) :
        if(self.phase==-1):# phase d'initialisation
            self.xPos0 = xPos
            self.yPos0 = yPos
            print("phaseAccel")
            self.phase = 0

        #calcul de la distance parcourue
        dx = xPos - self.xPos0
        dy = yPos - self.yPos0
        d0 = np.sqrt(dx*dx + dy*dy)

        #calcul de la distance jusqu'à la cible
        dx = self.xCible - xPos
        dy = self.yCible - yPos
        dCible = np.sqrt(dx*dx+dy*dy)

        # calcul des vitesses
        if(dCible == 0) : return 0,0
        vX = self.vMax * dx / dCible
        vY = self.vMax * dy / dCible

        if(self.phase == 0): # phase d'accélération
            oldV = np.sqrt(vX_old*vX_old+vY_old*vY_old)
            v = np.sqrt(vX*vX+vY*vY)
            if (abs(v-oldV)<0.001*self.vMax) : # on a atteint la vitesse maximale
                self.dAccel = d0
                print("phase vit constante")
                self.phase = 1

            if (dCible<=d0): # la moitié de la distance a été parcourue, on décélère
                self.dAccel = d0
                print("phaseDecel")
                self.phase = 2

        if(self.phase == 1 and dCible<self.dAccel) : # phase de vitesse constante

            self.phase = 2
            self.dAccel = 0
            print("phaseDecel")

        if(self.phase==2): # phase de décélération
            vX,vY = setAmaxXY(self.resolution,self.aMax,0,vX_old,0,vY_old)

            # en fin de parcours, on ajuste précisément pour tomber exactement sur la cible
            xPosPrevu = xPos+calcNPas(vX)*self.resolution
            yPosPrevu = yPos+calcNPas(vY)*self.resolution

            if(xPos==self.xCible): vX = 0
            elif(vX>0 and xPosPrevu>self.xCible): vX = 50
            elif(vX<0 and xPosPrevu<self.xCible): vX = -50
            elif(vX == 0 and xPosPrevu<self.xCible) : vX = 50
            elif(vX == 0 and xPosPrevu>self.xCible) : vX = -50

            if(yPos==self.yCible) : vY = 0
            elif(vY>0 and yPosPrevu>self.yCible): vY = 50
            elif(vY<0 and yPosPrevu<self.yCible): vY = -50
            elif(vY == 0 and yPosPrevu<self.yCible) : vY = 50
            elif(vY == 0 and yPosPrevu>self.yCible) : vY = -50

        else :
            vX,vY = setAmaxXY(self.resolution,self.aMax,vX,vX_old,vY,vY_old)

        if(vX==0 and vY==0) : self.phase = 3
        self.index +=1
        return vX,vY
