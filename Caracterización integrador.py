# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 11:56:51 2021

@author: Luca y Maia
"""

#Para caracterizar el integrador, fijar un pulso cuadrado en el GF de 50 Hz y 4 Vrms.

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
print('Fijate que salgan los cuadraditos y el triangulito')
#%%

#Para guardar los datos

mediciones=np.zeros([3,2500])
mediciones=[tiempo,data1V,data2V]
mediciones=np.transpose(mediciones)
df=pd.DataFrame(mediciones)
#print(time.localtime())
df.to_csv('Caracterización.csv')
