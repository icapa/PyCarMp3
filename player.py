#!/usr/bin/python
import os
import commands
import time
import threading
import thread
import random
from subprocess import Popen, PIPE, STDOUT
from socket import *
#-------------------------------------------------------------------
# Funcion para imprimir la lista de ficheros separado en directorios
#-------------------------------------------------------------------
def DebugLista(laLista):
	indice=0
	print 'Total de directorios' + str(len(laLista))
	for a in laLista:
		indice=indice+1
		print 'Directorio ' + str(indice) + '-->'
		print 'Total de ficheros en directorio: ' + str(len(a))
		for b in a:
			print '\t'+b

#----------------------------------------------------
# Funcion para crear la lista cogiendo los ficheros
#----------------------------------------------------
def CreaLista(ruta):
	array_ficheros=[]
	array_directorios=[]
	directorios = sorted(os.listdir(raiz))
	for un_dir in directorios:
		if os.path.isdir(raiz+un_dir):

			directorio_interno = sorted(os.listdir(raiz+un_dir))
			array_ficheros=[]
			for f_interno in directorio_interno:
				nombre_fichero=raiz+un_dir+'/'+f_interno
				if nombre_fichero[-1]=='\n':
					nombre_fichero = nombre_fichero[:-1]
				array_ficheros.append(nombre_fichero)	
			array_directorios.append(array_ficheros)
	return array_directorios

#--------------------------------------------------------------------
# Funcion que devuelve nombre de fichero,pasando indice de directorio
# y el indice del fichero
#--------------------------------------------------------------------
def DameFichero(lista_ficheros,indice_dir,indice_file):
	debug_file=(lista_ficheros[indice_dir])[indice_file]
	print 'DameFichero -> ' + debug_file
	return debug_file
	

#-------------------------------------------------------------------
# Reproduce un fichero y devuelve el descriptor para tratar sobre el
#-------------------------------------------------------------------
def PlayFichero(player,fichero):
	p = Popen([player,'-o','local',fichero],stdout=PIPE,stdin=PIPE,stderr=STDOUT)
	#print player,fichero
	#p = Popen([player,fichero],stdout=PIPE,stdin=PIPE,stderr=STDOUT)
	return p

#---------------------------------------------------
# Para la reproduccion
#---------------------------------------------------
def StopReproduccion(p):
	grep_stdout = p.communicate(input='q')[0]
	return grep_stdout

#------------------------------------------------------
# Devuelve una lista completa para el shuffle completo
#------------------------------------------------------
#def GeneraListaCompleta(lista_ficheros):
#	indice=0
#	indice_dir=0
#	indice_en_dir=0
#	lista_completa=[]
#	print 'El numero de elementos es:' + str(len(lista_ficheros))
#	for i in lista_ficheros:
#		print 'Vamos por indice de directorio: ' + str(indice_dir)
#		print 'Numero de elementos en el directorio: ' + str(len(i))
#		indice_en_dir=0;
#		for j in i:
#			lista_completa.append([indice,indice_dir,indice_en_dir,j])
#			indice=indice+1
#			indice_en_dir=indice_en_dir+1;
#		indice_dir=indice_dir+1		
#	
#	# Esto hace el debug de la lista
#	#for p in lista_completa:
#	#	print p
#	return lista_completa

#--------------------------------------------
# Thread que maneja las comunicaciones
#--------------------------------------------
def HiloComunicaciones(valor1,valor2):
	global modo
	global siguiente_usuario
	BUFF=1024
	HOST=''
	PORT=9999
	ADDR = (HOST,PORT)
	serversock = socket(AF_INET,SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	serversock.bind(ADDR)
	serversock.listen(5)

	while 1:
		print 'Esperando conexion...'
		clientsock,addr = serversock.accept()
		print 'Conectado...',addr
		while 1:
			data = clientsock.recv(BUFF)
			if not data:
				print 'Socket Recv Error!!!'
				break
			print 'data:' + repr(data)
			if 'next_file' in data:
				print 'Siguiente cancion'
				siguiente_usuario=1 #esto es hacia adelante
				StopReproduccion(p)
			elif 'prev_file' in data:
				print 'Anterior cancion'
				siguiente_usuario=2
				StopReproduccion(p)
			elif 'next_folder' in data:
				print 'Carpeta siguiente'
				siguiente_usuario=3
				StopReproduccion(p)
			elif 'prev_folder' in data:
				print 'Carpeta anterior'
				siguiente_usuario=4
				StopReproduccion(p)
			elif 'modo' in data:
				sModo = data.split("=")
				if len(sModo)==2:
					elModo = int(sModo[1])
					if elModo>=0 and elModo<4:
						modo=elModo
						print 'Cambiando a modo: '+str(modo)

				



			
#-------------------------------------
# La logica para la siguiente cancion
#------------------------------------
def SiguienteCancion(adelante):
	global lista_ficheros		#Esto esta separado en directorios
	global indice_directorio	#Indice directorio actual
	global indice_fichero		#Indice fichero actual dentro del directorio
	global modo					# 
	
	if modo==0:					# Modo contiguo
		print 'Modo 0: Continuo todo el disco'
		if indice_directorio==-1:
			indice_fichero=0
			indice_directorio=0
		else:
			# Siguiente arriba
			if adelante==True:
				if indice_fichero==len(lista_ficheros[indice_directorio])-1:	# Es el ultimo
					if indice_directorio==len(lista_ficheros)-1:
						indice_directorio=0
					else:
						indice_directorio=indice_directorio+1
					indice_fichero=0
				else:
					indice_fichero=indice_fichero+1
			else:
				# Si es hacia atras
				if indice_fichero==0:
					if indice_directorio==0:
						indice_directorio=len(lista_ficheros)-1
					else:
						indice_directorio=indice_directorio-1
				else:
					indice_fichero=indice_fichero-1
	elif modo==1:				# Modo directorio
		print 'Modo 1: Continuo directorio'
		
		if indice_directorio==-1:
			indice_fichero=0
			indice_directorio=0
		else:
			if adelante==True:
				if indice_fichero==len(lista_ficheros[indice_directorio])-1:
					indice_fichero=0
				else:
					indice_fichero=indice_fichero+1
			else:
				if indice_fichero==0:
					indice_fichero=len(lista_ficheros[indice_directorio])-1
				else:
					indice_fichero=indice_fichero-1
	elif modo==2:
		print 'Modo 2: Aleatorio todo el disco'
		ran_dir = random.randint(0,len(lista_ficheros)-1)
		print 'Directorio entre 0 y ' + str(len(lista_ficheros)-1) + ' Salio: ' + str(ran_dir)
		ran_file = random.randint(0,len(lista_ficheros[ran_dir])-1)
		print 'Fichero entre 0 y ' + str(len(lista_ficheros[ran_dir])-1)+ ' Salio: ' + str(ran_file)
		indice_directorio=ran_dir
		indice_fichero=ran_file
	elif modo==3:
		if indice_directorio==-1:	# Si es la primera vez
			indice_directorio=0
		print 'Modo 3: Aleatorio directorio'
		ran_file = random.randint(0,len(lista_ficheros[indice_directorio])-1)
		indice_fichero=ran_file
	return (lista_ficheros[indice_directorio])[indice_fichero]

#---------------------------------------------------------------
# Cambia de carpeta, adelante=True siguiente, si es false previo
#--------------------------------------------------------------
def SiguienteCarpeta(adelante):
	global indice_directorio
	global indice_fichero
	global lista_ficheros
	if modo==0 or modo==1 or modo==3: #odo normal, carpeta o aleatorio carpeta
		if indice_directorio==-1:
			indice_directorio=0
			indice_fichero=0
		else:
			if adelante==True:
				if indice_directorio==len(lista_ficheros)-1:
					indice_directorio=0
				else:
					indice_directorio=indice_directorio+1
			else:
				if indice_directorio==0:
					indice_directorio=len(lista_ficheros)-1
				else:
					indice_directorio=indice_directorio-1
			indice_fichero=0	# Siempre empezamos por la uno
	return (lista_ficheros[indice_directorio])[indice_fichero]


#############################################
########### Programa principal ##############
#############################################
raiz='/media/pendrive/'
player='/usr/bin/omxplayer'
#player='/usr/bin/mplayer'

lista_ficheros=CreaLista(raiz)
num_dir = len(lista_ficheros)

indice_directorio=-1
indice_fichero=-1
fichero_actual=''
p=-1
siguiente_usuario=0	# 0: No toco el usuario, 1: Movemos para arriba cancion 2: Movemos para abajo
modo=3	#0 continuo, 1 directorio actual, 2 aleatorio continuo, 3 aleatorio directorio
# Arrancamos el hilo de comunicaciones
thread.start_new_thread(HiloComunicaciones,(0,0))


while True:
	if num_dir!=0:
		print 'Hay '+str(num_dir)+' directorios de musica!!'
		while True:
			if siguiente_usuario==0:			# El usuario no toco se avanza normal
				nombre=SiguienteCancion(True)	
			elif siguiente_usuario==1:			# El usuario pulso hacia adelante
				print 'El usuario NEXT'
				nombre=SiguienteCancion(True)
				siguiete_usuario=0
			elif siguiente_usuario==2:			# El usuario pulso hacia atras
				print 'El usuario PREV'
				nombre=SiguienteCancion(False)
			elif siguiente_usuario==3:
				print 'El usuario Carpeta NEXT'
				nombre = SiguienteCarpeta(True)
			elif siguiente_usuario==4:
				print 'El usuario Carpeta PREV'
				nombre = SiguienteCarpeta(False)
			siguiente_usuario=0
			
				
			#-- Para saber lo que tocamos
			print '-----=====##########=====-----'
			print 'InDir  Num:  \t'+ str(indice_directorio)
			print 'InFile Num: \t'+ str(indice_fichero)
			print ' File Name:\t'+ nombre
			print '-----=====##########=====-----'
			#-- End ---
			
			p=PlayFichero(player,nombre)
			time.sleep(1)
			p.wait()
	else:

		lista_ficheros=CreaLista(raiz)
		num_dir = len(lista_ficheros)
		print '-- No hay ficheros para reproducir ... esperando --'
		time.sleep(2)	# No hay nada esperamos


