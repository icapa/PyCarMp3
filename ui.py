import pygame
from pygame.locals import *
import time
import threading
import thread
import sys
import os
import glob
import subprocess
from socket  import *
import errno
from socket import error as socket_error

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event2"
os.environ["SDL_MOUSEDRV"] = "TSLIB"


# Esto son los clicks calibrados
#Pulsado X: 33 Y: 184
#Pulsado X: 143 Y: 190
#Pulsado X: 89 Y: 161
#Pulsado X: 86 Y: 211
#Pulsado X: 218 Y: 165
#Pulsado X: 212 Y: 206
#Pulsado X: 288 Y: 187


#-- Asi es la agrupacion de botones
buttonFilePrev=[13,164,54,204]
buttonFileNext=[125,170,162,210]
buttonFolderNext=[66,141,106,181]
buttonFolderPrev=[66,191,106,233]
buttonPlay=[192,145,244,185]
buttonPause=[192,186,244,226]
buttonModo=[264,167,308,207]
buttonSalir=[0,0,20,20]

#-- Los meto todos en un array para la comparacion facil
buttons=[buttonFilePrev,buttonFileNext,buttonFolderNext,buttonFolderPrev,buttonPlay,buttonPause,buttonModo,buttonSalir]





#screen size
width  = 320
height = 240
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.init()
#disable mouse cursor
pygame.mouse.set_visible(False)
font = pygame.font.Font(None,26)
font_color=(255,0,0)
skin = pygame.image.load("/home/pi/PyCarMp3/PyCarMp3.png")
screen.blit(skin, (0, 0))
pygame.display.update()

#---------------------------------
# Renderizado el texto que llega
#---------------------------------
def RenderRecText(carpeta,cancion,modo):
	global protector
	if protector==False:
		s=pygame.Surface((290,94)) # Superficie para borrar

		s.fill((0,0,0))	# Negro
		screen.blit(s,(20,35))
		renCarpeta=font.render('['+carpeta+']',1,(font_color))
		screen.blit(renCarpeta,(23,40))
		renFile=font.render(cancion,1,(font_color))
		screen.blit(renFile,(23,65))
		renModo=font.render(modo,1,(font_color))
		screen.blit(renModo,(23,110))
		pygame.display.update()

#----------------------------------
# Funcion que se conecta al player
#--------------------------------
def ConnectPlayer():
	try:
		s = socket(AF_INET,SOCK_STREAM)
		s.connect(('127.0.0.1', 9999))
	except socket_error as serr:
		if serr.errno != errno.ECONNREFUSED:
			# Not the error we are looking for, re-raise
			raise serr
		s=-1

	return s


#---------------------------------------
# Funcion que envia el comando al player
#---------------------------------------
def SendToPlayer(elSocket,comando):
	try:
		elSocket.send(comando+'\n')	# Si no se puede enviar
	except socket_error as serr:
		return False
	return True


#-----------------------------------------
# Funcion que desglosa que boton se pulso
#-----------------------------------------
def BotonPulsado(touchPos):
	global buttons
	num=-1
	for a in buttons:
		num=num+1
		if a[0] <=touchPos[0] <= a[2]:
			if a[1] <= touchPos[1] <= a[3]:
				print 'Pulsado: ' + str(num)
				return num
	return -1

#---------------------------------------
# Hilo de recepcion de datos del player
#---------------------------------------
def RevFromPlayer(theSock,dummy):
	global gCarpeta
	global gFile
	global gModo
	while True:
		try:
			datos=theSock.recv(1024)
			if not datos:
				print 'Socket Recv Error'
				time.sleep(3)
			else:
				print 'Datos recibidos:'
				aaa=datos.split('\n')
				RenderRecText(aaa[0],aaa[1],aaa[2])
				gCarpeta=aaa[0]
				gFile=aaa[1]
				gModo=aaa[2]
		except socket_error as serr:
			print 'Socket Recv excepcion'
			time.sleep(3)
	# Aqui se 

	
	

#---------------------------------------
# Funcion que reacciona al boton pulsado
#---------------------------------------
def OnButton(id_boton):
	if id_boton==0:
		print 'Pulsado File Prev'
		return 'prev_file'
	if id_boton==1:
		print 'Pulsado File Next'
		return 'next_file'
	if id_boton==2:
		print 'Pulsado Folder Next'
		return 'next_folder'
	if id_boton==3:
		print 'Pulsado Folder Prev'
		return 'prev_folder'
	if id_boton==4:
		print 'Pulsado PLAY'
		return 'play'
	if id_boton==5:
		print 'Pulsado PAUSE'
		return 'pause'
	if id_boton==6:
		print 'Pulsado MODO'
		return 'modo'
	if id_boton==7:
		print 'Apagamos!!'
		system('sudo halt')
#-----=====##########=====-----
# 	Programa principal 
#-----=====##########=====-----

# Conectamos al socket
#
while True:
	theSock = ConnectPlayer()
	if theSock!=-1:
		print ' Conexion correcta a socket'
		break
	else:
		print 'Error, no hay player !!'
		time.sleep(3)
thread.start_new_thread(RevFromPlayer,(theSock,0))


pygame.time.set_timer(USEREVENT+1,5000)
minutos=0
protector_minutos=12 # 1 minutos
protector=False

while True:
	# Gestion de los eventos
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			if minutos<protector_minutos:
				minutos = minutos +1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if protector==False:
				minutos=0
				touchPos=(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
				print 'Pulsado X: '+str(touchPos[0])+' Y: '+str(touchPos[1])
				theButton = BotonPulsado(touchPos)
				comando=OnButton(theButton)
				if SendToPlayer(theSock,comando)==True:
					print 'Comando enviado OK'
				else:
					print 'Comando enviado ERROR'
			else:
				# Repintamos
				print 'Salimos de Salva Pantallas'
				protector=False
				screen.blit(skin, (0, 0))
				pygame.display.update()
				protector=False
				RenderRecText(gCarpeta,gFile,gModo)
				pygame.display.update()
	if minutos == protector_minutos:
		minutos = minutos+1 # Lo hago para que solo pase una vez
		print 'Protege pantallas !!'
		protector=True
		s=pygame.Surface((320,240)) # Superficie para borrar
		s.fill((0,0,0))	# Negro
		screen.blit(s,(0,0))
		pygame.display.update()

	time.sleep(0.1)
