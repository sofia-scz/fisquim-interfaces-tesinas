import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
plt.style.use('classic')
###############################################################################################
num = 0
Temp = 0
Title = str(num)+'T-' + str(Temp)+'K- '
###############################################################################################
Kb = 8.617333262*10**(-5)

capas = 4
at = (capas-1)*6+3

Ecin = at*1.5*Kb*Temp
###############################################################################################
# Energia Cientica -  Energia Potencial - Temperatura
###############################################################################################
data1 = pd.read_csv("Ekin_histogram.out",delim_whitespace=True, header=None)

data2 = pd.read_csv("Epot_histogram.out",delim_whitespace=True, header=None)

data3 = pd.read_csv("temperature_histogram.out",delim_whitespace=True, header=None)

#plt.title('Frecuencia')
plt.xlabel('E')
plt.ylabel('cuentas')
plt.scatter(data1[0],data1[1])
plt.axvline(Ecin ,color="purple",label = 'Equiparticion')
plt.legend()
plt.title(Title+'Ekin_histogram')
plt.savefig(Title + "Ekin_histogram.png")
plt.clf()

plt.xlabel('E')
plt.ylabel('cuentas')
plt.scatter(data2[0],data2[1])
plt.axvline(Ecin ,color="purple",label = 'Equiparticion')
plt.legend()
plt.title(Title + "Epot_histogram")
plt.savefig(Title + "Epot_histogram.png")
plt.clf()

plt.xlabel('E')
plt.ylabel('cuentas')
plt.scatter(data1[0],data1[1],color='red',label='E kin')
plt.scatter(data2[0],data2[1],color='blue',label='E pot')
plt.axvline(Ecin ,color="purple",label = 'Equiparticion')
plt.title(Title + "E_histogram")
plt.legend()
plt.savefig(Title + "E_histogram.png")
plt.clf()

plt.xlabel('E')
plt.ylabel('cuentas')
plt.scatter(data3[0],data3[1])
plt.title(Title + "temperature_histogram")
plt.savefig(Title + "temperature_histogram.png")
plt.clf()
###############################################################################################
# Movimiento de los atomos de las primeras 3 capas
#Para cada configuracion del slabmotion se compara con la conf de eq. inicial
# Las tablas contienen Desplazamiento en Angstroms - histograma normalizado - cuentas.
# Posición - desplazamiento relativo.
# - 1 - Ridge 
# - 2 - Facet
# - 3 - Valley
# 
# hacer histograma segun red de brave: X - 4.02   Y - 2.84   Z (capa)
###############################################################################################
#X = Coordenate - N = Layer  #header=None
X1 = pd.read_csv("x_layer001_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion X1" , 1 : "Desp X1" ,2 : "cuentas X1"}
X1.rename(columns=dic,inplace=True)

Y1 = pd.read_csv("y_layer001_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Y1" , 1 : "Desp Y1" ,2 : "cuentas Y1"}
Y1.rename(columns=dic,inplace=True)

Z1 = pd.read_csv("z_layer001_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Z1" , 1 : "Desp Z1" ,2 : "cuentas Z1"}
Z1.rename(columns=dic,inplace=True)

X2 = pd.read_csv("x_layer002_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion X2" , 1 : "Desp X2" ,2 : "cuentas X2"}
X2.rename(columns=dic,inplace=True)

Y2 = pd.read_csv("y_layer002_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Y2" , 1 : "Desp Y2" ,2 : "cuentas Y2"}
Y2.rename(columns=dic,inplace=True)

Z2 = pd.read_csv("z_layer002_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Z2" , 1 : "Desp Z2" ,2 : "cuentas Z2"}
Z2.rename(columns=dic,inplace=True)

X3 = pd.read_csv("x_layer003_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion X3" , 1 : "Desp X3" ,2 : "cuentas X3"}
X3.rename(columns=dic,inplace=True)

Y3 = pd.read_csv("y_layer003_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Y3" , 1 : "Desp Y3" ,2 : "cuentas Y3"}
Y3.rename(columns=dic,inplace=True)

Z3 = pd.read_csv("z_layer003_histo_mov.out",delim_whitespace=True,header=None)
dic = {0: "Posicion Z3" , 1 : "Desp Z3" ,2 : "cuentas Z3"}
Z3.rename(columns=dic,inplace=True)

R1= pd.concat([X1,Y1,Z1], axis=1)
R2= pd.concat([X2,Y2,Z2], axis=1)
R3= pd.concat([X3,Y3,Z3], axis=1)
X= pd.concat([X1,X2,X3], axis=1)
Y= pd.concat([Y1,Y2,Y3], axis=1)
Z= pd.concat([Z1,Z2,Z3], axis=1)
###############################################################################################
##                               #PLOT DISPLACEMENTS####                  ####################
###############################################################################################
plt.style.use('seaborn-whitegrid')
#plt.axvline(4.02 ,color="purple")
#plt.axvline(-4.02 ,color="purple")
plt.xlabel("Posicion X")
plt.ylabel("cuentas X")
plt.plot(R1["Posicion X1"], R1 ["Desp X1"], color = "r", label= "Ridge")
plt.plot(R2["Posicion X2"], R2 ["Desp X2"], color = "g", label= "Facet")
plt.plot(R3["Posicion X3"], R3 ["Desp X3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en X')
plt.savefig(Title + "X.png")
plt.clf()
#plt.axvline(4.02 ,color="purple")
#plt.axvline(-4.02 ,color="purple")
plt.xlabel("Posicion X1")
plt.ylabel("cuentas X1")
plt.plot(R1["Posicion X1"], R1 ["Desp X1"], color = "r", label= "Ridge")
plt.legend()
plt.title(Title+'Desplazamientos en X-Ridge')
plt.savefig(Title + "X1.png")
plt.clf()
#plt.axvline(4.02 ,color="purple")
#plt.axvline(-4.02 ,color="purple")
plt.xlabel("Posicion X2")
plt.ylabel("cuentas X2")
plt.plot(R2["Posicion X2"], R2 ["Desp X2"], color = "g", label= "Facet")
plt.legend()
plt.title(Title+'Desplazamientos en X-Facet')
plt.savefig(Title + "X2.png")
plt.clf()
#plt.axvline(4.02 ,color="purple")
#plt.axvline(-4.02 ,color="purple")
plt.xlabel("Posicion X3")
plt.ylabel("cuentas X3")
plt.plot(R3["Posicion X3"], R3 ["Desp X3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en X-Valley')
plt.savefig(Title + "X3.png")
plt.clf()

#
#plt.axvline(-2.84,color="purple")
plt.xlabel("Posicion Y")
plt.ylabel("cuentas Y")
plt.plot(R1["Posicion Y1"], R1 ["Desp Y1"], color = "r", label= "Ridge")
plt.plot(R2["Posicion Y2"], R2 ["Desp Y2"], color = "g", label= "Facet")
plt.plot(R3["Posicion Y3"], R3 ["Desp Y3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en Y')
plt.savefig(Title + "Y.png")
plt.clf()
#plt.axvline(-2.84,color="purple")
plt.xlabel("Posicion Y")
plt.ylabel("cuentas Y")
plt.plot(R1["Posicion Y1"], R1 ["Desp Y1"], color = "r", label= "Ridge")
plt.legend()
plt.title(Title+'Desplazamientos en Y-Ridge')
plt.savefig(Title + "Y1.png")
plt.clf()
#plt.axvline(-2.84,color="purple")
plt.xlabel("Posicion Y2")
plt.ylabel("cuentas Y2")
plt.plot(R2["Posicion Y2"], R2 ["Desp Y2"], color = "g",label= "Facet")
plt.legend()
plt.title(Title+'Desplazamientos en Y-Facet')
plt.savefig(Title + "Y2.png")
plt.clf()
#plt.axvline(-2.84,color="purple")
plt.xlabel("Posicion Y3")
plt.ylabel("cuentas Y3")
plt.plot(R3["Posicion Y3"], R3 ["Desp Y3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en Y-Valley')
plt.savefig(Title + "Y3.png")
plt.clf()


plt.xlabel("Posicion Z")
plt.ylabel("cuentas Z")
plt.plot(R1["Posicion Z1"], R1 ["Desp Z1"], color = "r", label= "Ridge")
plt.plot(R2["Posicion Z2"], R2 ["Desp Z2"], color = "g", label= "Facet")
plt.plot(R3["Posicion Z3"], R3 ["Desp Z3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en Z')
plt.savefig(Title + "Z.png")
plt.clf()

plt.xlabel("Posicion Z1")
plt.ylabel("cuentas Z1")
plt.plot(R1["Posicion Z1"], R1 ["Desp Z1"], color = "r", label= "Ridge")
plt.legend()
plt.title(Title+'Desplazamientos en Z-Ridge')
plt.savefig(Title + "Z1.png")
plt.clf()

plt.xlabel("Posicion Z2")
plt.ylabel("cuentas Z2")
plt.plot(R2["Posicion Z2"], R2 ["Desp Z2"], color = "g", label= "Facet")
plt.title(Title+'Desplazamientos en Z-Facet')
plt.legend()
plt.savefig(Title + "Z2.png")
plt.clf()

plt.xlabel("Posicion Z3")
plt.ylabel("cuentas Z3")
plt.plot(R3["Posicion Z3"], R3 ["Desp Z3"], color = "b", label= "Valley")
plt.legend()
plt.title(Title+'Desplazamientos en Z-Valley')
plt.savefig(Title + "Z3.png")
plt.clf()





