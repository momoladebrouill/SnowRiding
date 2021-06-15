import pygame as pg
import math

from colorsys import hsv_to_rgb
from noise import pnoise1





def boule(surface,x,y,rayon):
	nb=int(rayon)
	for i in range(nb):
		
		gotox=math.cos(2*math.pi*i/nb)
		gotoy=math.sin(2*math.pi*i/nb)
		c=hsv_to_rgb(i/nb,1,(100-rayon)/100*255)
		pg.draw.rect(surface,c,pg.Rect((int(x+gotox*rayon),int(y+gotoy*rayon)),(10,10)))





if __name__=="__main__":
	# Constantes :
	FPS = 60  # les fps tabernak
	WIND = 750 # dimentions de la fentere    
	x=0
	pg.init()
	f = pg.display.set_mode(size=(WIND, WIND))
	pg.display.set_caption("Gravitation autour du plus fat")
	fpsClock = pg.time.Clock()
	font = pg.font.Font('../consolas.ttf', 30) #police//roxane
	depx,depy=WIND/2,WIND/2#la caméra
	zoom=1
	mouv=10
	b = True
	lutins=list()  
	x=0
	try:
		while b:
			# Actualiser:
			pg.display.flip()

			# Appliquer les images de fond sur la fenetre
			s = pg.Surface((WIND, WIND))  # piqué sur stackoverflow pour avoir un fond avec un alpha

			text = font.render(str(len(lutins)), True, (0,0,0))
			textRect = text.get_rect()

			p = pg.key.get_pressed()  # SI la touche est appuyée
			antdep=(depx,depy)
			if p[pg.K_d]:depx-=mouv
			if p[pg.K_q]:depx+=mouv
			if p[pg.K_z]:depy+=mouv
			if p[pg.K_s]:depy-=mouv



			s.set_alpha(50)
			s.fill((0, 0, 0))
			f.blit(s, (0, 0))
			pointer=pg.mouse
			pos=pointer.get_pos()

			for event in pg.event.get():  # QUAND la touche est appuyée
				if event.type == pg.QUIT:
					b = False
					print(" Fin du jeu  babe")
				elif event.type == pg.KEYUP:
					"""if event.dict['key']==pg.K_SPACE:

                                                        if event.dict['key']==pg.K_a:"""

				elif event.type==pg.MOUSEBUTTONUP:
					"""if event.button==1: #click gauche
                                                            pos=event.pos




                                                        if event.button==3: #click droit
                                                           """
					if event.button==4: #vers le haut
						zoom+=10
					elif event.button==5: #vers le bas
						zoom-=10
			zoom=pnoise1(x/1000)*WIND/2
			#zoom=zoom%(WIND/2)
			x+=1
			x=x%1000
			boule(f,WIND/2,WIND/2,zoom)
			""" i in range(nb):
					gotox=math.cos(2*math.pi*i/nb)
					gotoy=math.sin(2*math.pi*i/nb)
					c=hsv_to_rgb(i/nb,1,255)
					pg.draw.rect(f,c,pg.Rect((int(gotox*zoom)+depx,int(gotoy*zoom)+depy),(10,10)))"""

			f.blit(text, (0,0))


			fpsClock.tick(FPS)
	except :
		pg.quit()
		raise
	finally:
		pg.quit()
