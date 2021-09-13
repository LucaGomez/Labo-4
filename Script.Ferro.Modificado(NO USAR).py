# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:18:56 2021

@author: Publico
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:12:42 2021
@author: Luca, Maia
"""


import pyvisa as visa
import time
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


rm = visa.ResourceManager()

instrumentos = rm.list_resources()  
print(instrumentos)
# Esto lista todos los dispositivos disponibles, uno de los cuales
# deberia ser "USB0::0x0699::0x0368::C017044::INSTR", donde los terminos
# indican "puerto::marca::modelo::nro_de_serie" del instrumento.

#%%

# Elijo el elemento que corresponde en instrumentos
#Con ese nombre abro el vinculo con el osciloscopio y el multimetro

osci=rm.open_resource(instrumentos[0])
multi=rm.open_resource(instrumentos[2])
#osc=rm.open_resource('USB0::0x0699::0x0363::C065093::INSTR')
#chequeo la comunicación
print('Osciloscopio:', osci.query('*IDN?'))
print('Multímetro:', multi.query('*IDN?'))
print('Chequear que estén bien definidos')

#MEDIMOS
#para leer las curvas del canal 1 y 2 necesito tomar los datos de la configuración
xze,xin=osci.query_ascii_values('WFMPRE:XZE?;XIN?',separator=';') #conf. base de tiempo
yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:CH1:YZE?;YMU?;YOFF?',separator=';') #conf. vertical canal 1
yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';') #conf. vertical canal 2
#dc = float(multi.query('MEASURE:VOLTAGE:DC?')) #Fija al multímetro para medir corriente continua (TERMOCUPLA)
R = float(multi.query('MEASURE:FRESistance?'))
#R = float(multi.query('MEASURE:RESistance?')) #Fija al multímetro para medir resistencia (RESIST. PLAT)

## Modo de transmision: Binario (osea, la onda digitalizada)
osci.write('DAT:ENC RPB') 
osci.write('DAT:WID 1') 

#%%

#Chequeamos la medición para la temperatura. Primero con la termocupla:
'''
dc = float(multi.query('MEASURE:VOLTAGE:DC?')) 
#dc=0.8
#Fórmula para la temperatura en función de dc:
T=25.08355*dc+7.860106*10**(-2)*dc**2-0.2503131*dc**3 #Fórmula extraída de https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html
'''
R = float(multi.query('MEASURE:FRESistance?')) 
T = 2.59*R-259
print('La temperatura es', T)
print('Si mide la temperatura ambiente OK!!! Acordate que dc tiene que estar en mV!!!')

#%%

#Ahora probamos registrar la pantalla del osciloscopio.

#leo las curvas como datos binarios
osci.write('DAT:SOU CH1' )
data1=osci.query_binary_values('CURV?', datatype='B',container=np.array)
osci.write('DAT:SOU CH2')    
data2=osci.query_binary_values('CURV?', datatype='B',container=np.array)

#transformo los datos 
tiempo = xze + np.arange(len(data1)) * xin #tiempos en s
data1V=(data1-yoff1)*ymu1+yze1 #tensión canal 1 en V
data2V=(data2-yoff2)*ymu2+yze2 #tensión canal 2 en V 


#graficamos los datos
plt.plot(tiempo,data1V,label='Canal 1')
plt.plot(tiempo,data2V,label='Canal 2')
plt.legend()
plt.figure()
plt.plot(data1V, data2V)
print('Esta figura debería dibujar el cíclo de histeresis. Chequear')

#%%

# Medimos la señal que tenemos sin el monel en el transformador

#leo las curvas como datos binarios
osci.write('DAT:SOU CH1' )
data1=osci.query_binary_values('CURV?', datatype='B',container=np.array)
osci.write('DAT:SOU CH2')    
data2=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    
#transformo los datos 
tiempo = xze + np.arange(len(data1)) * xin #tiempos en s
data1V=(data1-yoff1)*ymu1+yze1 #tensión canal 1 en V
data2V=(data2-yoff2)*ymu2+yze2 #tensión canal 2 en V 
'''  
#Mido la temperatura (termocupla)
dc = float(multi.query('MEASURE:VOLTAGE:DC?')) 
#Fórmula para la temperatura en función de dc:
T=25.08355*dc+7.860106*10**(-2)*dc**2-0.2503131*dc**3 #Fórmula extraída de https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html
'''
#Mido la temperatura (RP)

R = float(multi.query('MEASURE:FRESistance?')) 
T = 2.59*R-259
#guardamos los datos
mediciones=np.zeros([3,2500])
mediciones=[tiempo,data1V,data2V]
mediciones=np.transpose(mediciones)
df=pd.DataFrame(mediciones)
#print(time.localtime())
df.to_csv('Medición sin monel.csv')

#%%

# Ahora deberíamos medir a mano cuánto tiempo tarda el monel en calentarse hasta temperatura ambiente. 
# En base a eso sabremos cada cuanto tiempo tomar mediciones. Por ejemplo:
# Si el monel tarda 10 minutos en calentarse, podríamos tomar mediciones cada 30 segundos, de esta forma tomamos 20 mediciones.

t = 12 #Tiempo de espera entre mediciones
N = 20 #Cantidad de mediciones

for i in range(N):
    #leo las curvas como datos binarios
    osci.write('DAT:SOU CH1' )
    data1=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    osci.write('DAT:SOU CH2')    
    data2=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    
    #transformo los datos 
    tiempo = xze + np.arange(len(data1)) * xin #tiempos en s
    data1V=(data1-yoff1)*ymu1+yze1 #tensión canal 1 en V
    data2V=(data2-yoff2)*ymu2+yze2 #tensión canal 2 en V 
    
    #Mido la temperatura
    #dc = float(multi.query('MEASURE:VOLTAGE:DC?')) 
    #Fórmula para la temperatura en función de dc:
    #T=25.08355*dc+7.860106*10**(-2)*dc**2-0.2503131*dc**3 #Fórmula extraída de https://srdata.nist.gov/its90/type_k/kcoefficients_inverse.html
    R = float(multi.query('MEASURE:FRESistance?')) 
    T = 2.59*R-259
    #guardamos los datos
    mediciones=np.zeros([3,2500])
    mediciones=[tiempo,data1V,data2V]
    mediciones=np.transpose(mediciones)

    df=pd.DataFrame(mediciones)
    #print(time.localtime())
    df.to_csv('Medición con temperatura '+str(T)+'.csv')
    
    time.sleep(t)
    
#Este bucle debería barrer N valores de temperatura, dejando t segundos entre cada medición.
#Al final, debería generar N archivos que tengan guardados los ciclos de interés, con la temperatura en el título del archivo.
    
#%%

Nt = 400
it = .5
t=[]
T=[]
currenttime=0
for i in range(Nt):
    R = float(multi.query('MEASURE:FRESistance?')) 
    Temp = 2.59*R-259
    t.append(currenttime)
    T.append(Temp)
    currenttime+=it
    time.sleep(it)
    
#%%
plt.plot(t, T)
