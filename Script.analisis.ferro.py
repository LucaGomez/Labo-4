# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 18:59:23 2021

@author: Luca
"""
import os
import numpy as np
import matplotlib.pyplot as plt
# ejemplo_dir = '/Users\Luca\Desktop\Facultad\Labo 4\Ferromagnetismo\Mediciones 08.09\Mediciones 08-09'
# contenido = os.listdir(ejemplo_dir)
# archivos = []
# for archivo in contenido:
#     if os.path.isfile(os.path.join(ejemplo_dir, archivo)) and archivo.endswith('.txt'):
#         archivos.append(archivo)
# print(archivos)

# Con los archivos dentro de una carpeta "mediciones":
archivos = os.listdir("mediciones")

#O sino, con los archivos en la misma carpeta:
# archivos = [i for i in os.listdir(".\\") if ".csv" in i]
print(archivos)

#%%
import re
T=[]
M=[]
for i in range (len(archivos)):
    file1=archivos[i]
    file=np.loadtxt("mediciones\\"+file1,dtype=float,delimiter = ',',skiprows= 1)
    t=file[:,1]
    V1=file[:,2]
    V2=file[:,3]
    plt.plot(V1,V2)
    plt.xlabel('V1')
    plt.ylabel('V2')
    
    '''
    plt.figure()
    plt.scatter(V1,V2)
    plt.title(archivos[i])
    '''
    #Estaría bueno poder pedirle al código que diga el mayor valor de V2 que se corresponde con V1, llamarlo 
    #M y hacer algo por el estilo:
    lista_lugar=np.where(V1==0)[0]   #Elige los indices que verifican V1=0, y luego toma el primero [0], esto es un array
    lugar=lista_lugar[0] #Define el lugar como el primer valor del array
    Mag=abs(V2[lugar]) #Define la magnetización como el valor absoluto de V2 evaluado en el índice definido
    M.append(Mag) #Lo agrega al vector de magnetización
    Te=[float(s) for s in re.findall(r'-?\d+\.?\d*', file1)] #Extrae el valor de temperatura del nombre del archivo
    T.append(Te) #Lo agrega al vector de temperaturas
    
#%%
plt.scatter(T,M)

'''
NOTA IMPORTANTE: ESTE CODIGO SOLO FUNCIONA CON ARCHIVOS NUMERADOS DESDE EL 1. NO LE GUSTAN ARCHIVOS CON OTRA
NUMERACION, COSA QUE ES UN PROBLEMA IMPORTANTE EN LA AUTOMATIZACION DEL TRABAJO.

PERO SI GUARDAMOS LAS MEDICIONES EN UNA CARPETA Y CORREMOS EL CÓDIGO DESDE LA MISMA CARPETA EN LA QUE ESTÁ
LA CARPETA DE MEDICIONES FUNCA JOYULI JOYULI, GRACIAS NICOOOOOOOO
'''
#%%
'''
import os
import numpy as np
import matplotlib.pyplot as plt
ejemplo_dir = '/Users\Luca\Desktop\Facultad\Labo 4\Ferromagnetismo\Mediciones 08.09\Mediciones con T en el nombre\En txt'
contenido = os.listdir(ejemplo_dir)
archivos = []
for archivo in contenido:
    if os.path.isfile(os.path.join(ejemplo_dir, archivo)) and archivo.endswith('.csv'):
        archivos.append(archivo)
print(archivos)
print(len(archivos))

#%%
Temp_archivo=[]
for i in range(len(archivos)):
    file=archivos[i]
    nuevo='/Users/Luca/Desktop/Facultad/Labo 4/Ferromagnetismo/Mediciones 08.09/Mediciones con T en el nombre/En txt'+'/'+str(i)+'.csv'
    Temp=[float(s) for s in re.findall(r'-?\d+\.?\d*', archivos[i])]
    Temp_archivo.append(Temp)
    
print(Temp_archivo)

#%%

for i in range(len(archivos)):
    nombre_archivo = i
    with open(nombre_archivo, "r") as archivo:
        # Omitir el encabezado
        next(archivo, None)
        for linea in archivo:
            # Remover salto de línea
            linea = linea.rstrip()
            # Ahora convertimos la línea a arreglo con split
            separador = ","
            lista = linea.split(",")
            # Tenemos la lista. En la 0 tenemos el nombre, en la 1 la calificación y en la 2 el precio
            V1 = lista[2]
            V2 = lista[3]
            plt.plot(V1,V2)
            plt.xlabel('V1')
            plt.ylabel('V2')
'''
