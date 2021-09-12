# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 18:59:23 2021

@author: Luca
"""


import os
import numpy as np
import matplotlib.pyplot as plt
ejemplo_dir = '/Users/Luca/Desktop/Facultad/Labo 4/Ferromagnetismo/Mediciones 08.09/Mediciones 08-09'
contenido = os.listdir(ejemplo_dir)
archivos = []
for archivo in contenido:
    if os.path.isfile(os.path.join(ejemplo_dir, archivo)) and archivo.endswith('.txt'):
        archivos.append(archivo)
print(archivos)

#%%
T=[]
V2=[]
for i in range (19):
    file1=archivos[i]
    file=np.loadtxt(file1,dtype=float,delimiter = ',',skiprows= 1)
    t=file[:,1]
    V1=file[:,2]
    V2=file[:,3]
    #plt.plot(V1,V2)
    
    plt.figure()
    plt.scatter(V1,V2)
    plt.title(archivos[i])
    
    #Estaría bueno poder pedirle al código que diga el mayor valor de V2 que se corresponde con V1, llamarlo 
    #V2m y hacer algo por el estilo:
    #V2m= algo
    #V2.append(V2m)
    #También deberíamos poder sacarle el valor de temperatura al nombre del archivo y meterlo en un vector de T
    #Te= algo con el nombre del archivo
    #T.append(Te)
    
#%%
