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
def DebugLista(lista_completa):
	indice=0
	print 'Total de directorios' + str(len(lista_completa))
	for a in lista_completa:
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
	directorios = os.listdir(raiz)
	for un_dir in directorios:
		if os.path.isdir(raiz+un_dir):

			directorio_interno = os.listdir(raiz+un_dir)
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
	return p

#---------------------------------------------------
# Para la reproduccion
#---------------------------------------------------
def StopReproduccion(p):
	grep_stdout = p.communicate(input='q')[0]
	return grep_stdout

#-----------------------------------------------------
# Devuelve si es la ultima cancion del directorio
#----------------------------------------------------
def UltimaCancion(lista_dicheros,directorio,fichero):
	actual_lista = lista_ficheros[directorio]
	if fichero==(len(actual_lista)-1):
		return True
	return False

#----------------------------------------------------
# Genera un par de numeros aleatorios para dir y file
#---------------------------------------------------
def GeneraShuffleFile(lista_completa):
	ran_file = random.randint(0,len(lista_completa)-1)
	registro = lista_completa[ran_file]
	print "Registro....:"
	print registro
	return registro

#------------------------------------------------------
# Devuelve una lista completa para el shuffle completo
#------------------------------------------------------
def GeneraListaCompleta(lista_ficheros):
	indice=0
	indice_dir=0
	indice_en_dir=0
	lista_completa=[]
	print 'El numero de elementos es:' + str(len(lista_ficheros))
	for i in lista_ficheros:
		print 'Vamos por indice de directorio: ' + str(indice_dir)
		print 'Numero de elementos en el directorio: ' + str(len(i))
		indice_en_dir=0;
		for j in i:
			lista_completa.append([indice,indice_dir,indice_en_dir,j])
			indice=indice+1
			indice_en_dir=indice_en_dir+1;
		indice_dir=indice_dir+1		
	
	# Esto hace el debug de la lista
	#for p in lista_completa:
	#	print p
	return lista_completa

#--------------------------------------------
# Thread que maneja las comunicaciones
#--------------------------------------------
def HiloComunicaciones(valor1,valor2):
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
			if not data: continue
			print 'data:' + repr(data)
			if 'next' in data:
				print 'Siguiente cancion'
				StopReproduccion(p)
			
#-------------------------------------
# La logica para la siguiente cancion
#------------------------------------
def SiguienteCancion():
	global lista_ficheros		#Esto esta separado en directorios
	global lista_completa		#Esto es una lista completa
	global indice_directorio	#Indice directorio actual
	global indice_fichero		#Indice fichero actual dentro del directorio
	return lista_completa[0]

#############################################
########### Programa principal ##############
#############################################
raiz='/media/pendrive/'
player='/usr/bin/omxplayer'

lista_ficheros=CreaLista(raiz)
num_dir = len(lista_ficheros)




indice_directorio=-1
indice_fichero=-1
fichero_actual=''
p=-1

modo=2	#0 continuo, 1 directorio actual, 2 aleatorio continuo, 3 aleatorio directorio
# Arrancamos el hilo de comunicaciones
#thread.start_new_thread(HiloComunicaciones,(0,0))


while True:
	if num_dir!=0:
		lista_completa=GeneraListaCompleta(lista_ficheros)
		print 'Hay '+str(num_dir)+' directorios de musica!!'
		indice_directorio=0
		indice_fichero=0


		while True:
			# Si es modo shuffle
			indice_total=SiguienteCancion()	# Esta hace toda la logistica
			#-- Para saber lo que tocamos
			print '-----=====##########=====-----'
			print 'Play Num: \t'+ str(indice_total[0]) 
			print 'Dir Num:  \t'+ str(indice_total[1])
			print 'File Num: \t'+ str(indice_total[2])
			print 'File Name:\t'+ indice_total[3]
			print '-----=====##########=====-----'
			p=PlayFichero(player,indice_total[3])
			#-- End ---
			time.sleep(2)
			p.wait()
	else:

		lista_ficheros=CreaLista(raiz)
		num_dir = len(lista_ficheros)
		print '-- No hay ficheros para reproducir ... esperando --'
		time.sleep(2)	# No hay nada esperamos


