#!/usr/bin/python
import os
import commands
import time
import threading
import random
from subprocess import Popen, PIPE, STDOUT
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
# Pasa a la siguiente cancion dentro de la carpeta
# devuelve indice de fichero. Directorio
# sera el mismo
#-----------------------------------------------------
def SiguienteCancion(lista_ficheros,directorio,fichero):
	actual_lista = lista_ficheros[directorio]	# Lista de dir actual
	if fichero== (len(actual_lista)-1):			# Si es la ultima
		return 0								# Volvemos al principio
	return fichero+1

#-----------------------------------------------------
# Pasa de directorio
#-----------------------------------------------------
def SiguienteDirectorio(lista_ficheros,directorio,fichero):
	if directorio==(len(lista_ficheros)-1):
		return 0
	directorio=directorio+1
	return directorio
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

while True:
	if num_dir!=0:
		lista_completa=GeneraListaCompleta(lista_ficheros)
		print 'Hay '+str(num_dir)+' directorios de musica!!'
		indice_directorio=0
		indice_fichero=0


		while True:
			# Si es modo shuffle
			indice_total=GeneraShuffleFile(lista_completa)
			print 'Reproduciendo !! ' + str(indice_total[0]) + ',' + str(indice_total[1])+','+str(indice_total[2])+','+indice_total[3]
#			fichero_actual=DameFichero(lista_ficheros,indice_total[0],indice_total[1])
			p=PlayFichero(player,indice_total[3])

			p.wait()

			#if UltimaCancion(lista_ficheros,indice_directorio,indice_fichero)==True:
			#	print 'Ultima cancion...pasamos de directorio'
			#	indice_directorio=SiguienteDirectorio(lista_ficheros,indice_directorio,indice_fichero)
			#	indice_fichero=0;
			#else:
			#	print 'Siguiente cancion'
				#indice_fichero=SiguienteCancion(lista_ficheros,indice_directorio,indice_fichero)
	else:

		lista_ficheros=CreaLista(raiz)
		num_dir = len(lista_ficheros)
		print '-- No hay ficheros para reproducir ... esperando --'
		time.sleep(2)	# No hay nada esperamos


