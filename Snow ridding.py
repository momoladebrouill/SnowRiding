import pygame as pg
import noise
import math
import random
import time
from cercle_trigoo import boule
from colorsys import hsv_to_rgb
# Constantes :
FPS = 50  # les fps tabernak
WIND = 750 # dimentions de la fentere
pg.init()

pg.mixer.pre_init()
pg.font.init()
f = pg.display.set_mode(size=(int(WIND*3/2), WIND))
pg.display.set_caption("SKIII")
perso=pg.image.load("assets/main3.png")
#perso=pg.transform.smoothscale(perso,(64,64))
imagRect=perso.get_rect()
#perso=pg.transform.rotozoom(perso,20,1)
fpsClock = pg.time.Clock()
font = pg.font.SysFont('consolas', 30) #police//roxane
b = True

LIMIYE=45
son=pg.mixer.Sound("assets/shwish.mp3")
yeah=pg.mixer.Sound("assets/pinwheel.mp3")
noo=pg.mixer.Sound("assets/confetti.mp3")
yeah.set_volume(0.01)
class Particule:
    def __init__(self,pos):
        self.cpos=Pos(pos.x,pos.y-40)
        self.score=1
        self.vec=Vec(5/16+random.random()/4,4*pentese*100)
    def draw(self):
        self.cpos.appliq(self.vec)
        pg.draw.rect(f,hsv_to_rgb(19/36,self.score,255),pg.Rect(self.cpos.x,self.cpos.y,3,3))
        self.score-=0.01
        return self.score>0
class Pos:
    def __init__(self,x=0,y=0,size=(10,10)):
        self.x=x
        self.y=y
        self.rect=pg.Rect((self.x,self.y),size)
    def appliq(self,force):
        self.x+=force.x
        self.y+=force.y
class Vec:
    def __init__(self,angl,intens):
        self.x=math.cos(angl*2*math.pi)*intens
        self.y=-math.sin(angl*2*math.pi)*intens
        self.c=hsv_to_rgb(random.random(),1,255)
    def draw(self,pos):
        pg.draw.line(f,self.c,(pos.x,pos.y),(pos.x+self.x*15,pos.y+self.y*15))

class Humanoide:
    def __init__(self):
        self.pos=Pos(WIND/2,10)
        self.grav=Vec(3/4,5)
        self.retour=Vec(1/2,6)
        self.confetis=[]
        self.ecart=0
        self.playing=30
        self.im=perso
        self.g=0
        self.orient=0 # angle en degre
        self.pente=0 # dervié en x
    def draw(self):
        self.pos.y+=self.g
        self.g+=0.1
        nextconf=[]
        for i in self.confetis:
            if i.draw():
                nextconf.append(i)
                
        antes=self.orient    
        pente=(piste[contact[1]+1].pos.y-piste[contact[1]-1].pos.y)/(piste[contact[1]+1].pos.x-piste[contact[1]-1].pos.x)
        orient=-math.degrees(math.asin(self.pente/30))*15
        self.ecart=abs(antes-orient)
        
        
        if self.pos.y>contact[0].y:
            if self.playing>0:
                self.playing-=1
            else:
                self.playing=30
                son.play()
            nextconf.append(Particule(self.pos))
            self.g=0
            self.pos.y=contact[0].y
            
            self.pente=pente
            self.orient=orient
            self.ecart=abs(antes-self.orient)
            if self.ecart>LIMIYE and self.ecart<360-LIMIYE:
                global b
                b=False
                              
                
            if self.pente>0:
                self.retour=Vec(0,6)
            else:
                self.retour=Vec(1/2,6)
        else:
            self.playing=20
            son.stop()
        self.confetis=nextconf[:]
        return self.pente
    def dessin(self):
        im=pg.transform.rotate(self.im,self.orient)
        f.blit(im,pg.Rect(self.pos.x,self.pos.y-100,1000,1000))
        
 
class Neige:
    taille=10
    def __init__(self,x):
        self.pos=Pos(x,0)
        self.pos.y=noise.pnoise1(place+x/WIND)*WIND+self.pos.x
    def draw(self):
        self.pos=Pos(self.pos.x,WIND-10,(self.taille,-self.pos.y))
        self.pos.y=noise.pnoise1(place+self.pos.x/WIND)*WIND/2+self.pos.x/2+WIND/4+50
        pg.draw.rect(f,(255,255,255),pg.Rect(self.pos.x,self.pos.y,self.taille,WIND-self.pos.y),border_radius=1)
    def line(self,lieu):
        if lieu-1 >=0 and lieu+1<len(piste)-1:
            for i in range(10):
                coul=(10-i)*25.5
                pg.draw.line(f,(coul,coul,coul),
                             (piste[lieu+1].pos.x+i*15,
                              piste[lieu+1].pos.y),
                             (piste[lieu-1].pos.x+i*15,
                              piste[lieu-1].pos.y),15)
            pg.draw.line(f,(255,255,255),(self.pos.x,self.pos.y),(piste[lieu-1].pos.x,piste[lieu-1].pos.y),15)
  
place=0
piste=[]
IsExpert=False
roger=Humanoide()
pentese=0.01
score=0
score_particules=[]
boom=0
for i in range(-20,int(94*3/2)):
    piste.append(Neige(i*8))
text = font.render("Snow Ridding", True, (255,255,255))
f.blit(text,(WIND/2,WIND/2))
s = pg.Surface((WIND*3/2, WIND))
s.set_alpha(1)
s.fill((0, 0, 0))
for i in range(256):
    pg.display.flip()
    f.blit(perso,(WIND/2,20))
    f.blit(s, (0, 0))
    time.sleep(0.01)
try:
    pg.mixer.music.load("assets/Last Train Home.mp3")
    pg.mixer.music.set_volume(0.05)
    pg.mixer.music.play(-1)    
    while b:
        # Actualiser:
        if b:
            pg.display.flip()
            pg.display.update()
        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND*3/2, WIND))  
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))

        if boom:
            if boom>100:
                boom=0
            else:
                boule(f,boom_pos[0],boom_pos[1],boom)
                boom+=2        
        indx=0
        for i in piste:
            
            if int(i.pos.x/10)==int(roger.pos.x/10):
                contact=(Pos(i.pos.x,i.pos.y),indx)
                roger.dessin()
            i.draw()
            i.line(indx)
            indx+=1
            
        
        if IsExpert:
            roger.grav.draw(roger.pos)
            roger.retour.draw(roger.pos)
            Vec(math.radians(roger.orient)/math.tau,10).draw(contact[0])
            for i in roger.confetis:
                i.vec.draw(i.cpos)
            pg.draw.rect(f,(0,255,0),(contact[0].x,contact[0].y,Neige.taille,100))
            pg.draw.rect(f,(255,0,0),pg.Rect(roger.pos.x,roger.pos.y,10,10))
            pente=(piste[contact[1]+1].pos.y-piste[contact[1]-1].pos.y)/(piste[contact[1]+1].pos.x-piste[contact[1]-1].pos.x)
            orient=-math.degrees(math.asin(pente/30))            
            text = font.render("Vitesse:"+format(pentese*100,"02")[:5]+
                               " ecart:"+str(int((roger.ecart)))+
                               " deg:"+str(int(roger.orient))+
                               " FPS:"+str(int(fpsClock.get_fps()))
                               , True, (255,255,255))
            textRect = text.get_rect()
            f.blit(text, (0,0))
        else:
            coul=(255,255,255)
            if boom:
                coul=hsv_to_rgb(boom/100,1,255)
            text = font.render(str(int(place))+"m", True, coul)
            textRect = text.get_rect()
            f.blit(text, (WIND*3/2-textRect.width,0))
            text = font.render(str(score), True, coul)
            textRect = text.get_rect()
            f.blit(text, (WIND*3/2-textRect.width,textRect.height))            
       
       
        pentese+=roger.draw()/10000000
        place+=pentese
        
        p = pg.key.get_pressed()  # SI la touche est appuyée
        if p[pg.K_d]:
            roger.pos.x+=10
        if p[pg.K_q]:
            roger.pos.x-=10
        if p[pg.K_k]:
            pentese+=0.0001
        if p[pg.K_SPACE]:
            roger.orient+=5#pentese*100
            if roger.orient>340:
                pentese+=0.001
                score+=1
                roger.orient=0
                boom=1
                boom_pos=roger.pos.x+imagRect.width/2,roger.pos.y+imagRect.height/2-100
                yeah.play()
        
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b=False
                roger.g=69
                pg.quit()
            if event.type==pg.KEYDOWN:
                if event.dict['key']==pg.K_SPACE:
                    if roger.pos.y>contact[0].y-1:
                        roger.g=-5 
            elif event.type == pg.KEYUP:
                if event.dict['key']==pg.K_w:
                    if not IsExpert:
                        pg.mixer.music.fadeout(1000)
                    else:
                        pg.mixer.music.play(-1)
                    IsExpert= not IsExpert
        fpsClock.tick(FPS)
        
except :
    raise
finally:
    if not roger.g==69:
        pg.mixer.music.stop()
        noo.play()
        print(roger.ecart)
        text = font.render("Perdu!", True, (255,0,0))
        textRect = text.get_rect()
        f.blit(text, (WIND/2,WIND/2))
        pg.display.flip()
        pg.time.delay(2000)
pg.quit()
