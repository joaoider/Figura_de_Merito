# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Calculo da resistividade e condutividade eletrica

import numpy as np
import math
from scipy.optimize import curve_fit

name = 'IV'

name1 = 'IV1'
# carrega dados experimentais do arquivo txt
data1 = np.loadtxt(name1+'.txt', comments='#')
voltage1 = data1[:,0]   # coluna 1 - voltage
current1 = data1[:,1]  # coluna 2 - current

name2 = 'IV2'
# carrega dados experimentais do arquivo txt
data2 = np.loadtxt(name2+'.txt', comments='#')
voltage2  = data2[:,0]   # coluna 1 - voltage
current2 = data2[:,1]  # coluna 2 - current

name3 = 'IV3'
# carrega dados experimentais do arquivo txt
data3 = np.loadtxt(name3+'.txt', comments='#')
voltage3  = data3[:,0]   # coluna 1 - voltage
current3 = data3[:,1]  # coluna 2 - current

name4 = 'IV4'
# carrega dados experimentais do arquivo txt
data4 = np.loadtxt(name4+'.txt', comments='#')
voltage4  = data4[:,0]   # coluna 1 - voltage
current4 = data4[:,1]  # coluna 2 - current

name5 = 'IV5'
# carrega dados experimentais do arquivo txt
data5 = np.loadtxt(name5+'.txt', comments='#')
voltage5  = data5[:,0]   # coluna 1 - voltage
current5 = data5[:,1]  # coluna 2 - current

w = 0.00001 # espessura em centímetros (100 nm)
a = 2.49 #cm comprimento (paralelo aos pinos)
d = 1.71 #cm largura (perpendicular aos pinos)
s = 0.39 #cm espaçamento entre os pinos

def linear(x, a, b):
    return a * x + b

# Ajuste linear
popt1, pcov1 = curve_fit(linear, voltage1, current1)
popt2, pcov2 = curve_fit(linear, voltage2, current2)
popt3, pcov3 = curve_fit(linear, voltage3, current3)
popt4, pcov4 = curve_fit(linear, voltage4, current4)
popt5, pcov5 = curve_fit(linear, voltage5, current5)


# Calculando Resitências e Condutâncias
R1 = 1./popt1[0]
print('resistencia', R1)
G1 = 1./R1
print('condutancia', G1)

R2 = 1./popt2[0]
print('resistencia', R2)
G2 = 1./R2
print('condutancia', G2)

R3 = 1./popt3[0]
print('resistencia', R3)
G3 = 1./R3
print('condutancia', G3)

R4 = 1./popt4[0]
print('resistencia', R4)
G4 = 1./R4
print('condutancia', G4)

R5 = 1./popt5[0]
print('resistencia', R5)
G5 = 1./R5
print('condutancia', G5)

"""
#### CALCULO MODELO 1, para amostras circulares de dimensões semi-infinitas

# Se o substrato for isolante
f1 =  (math.log(2)) / math.log(math.sinh(w/s) / math.sinh(w/(2*s)))
print('f1 é: ', f1)
# Aproximação para w << s -> f1=1
#f1 = 1
f2 = 1  # pq d/s >> 1 , > 4

# Condutividades e Resistividades
sigma1 = G1 * math.log(2) / (math.pi * w * f1 * f2)
rho1 = ( math.pi * w * R1 * f1 * f2 ) / ( math.log(2) )
sigma2 = G2 * math.log(2) / (math.pi * w * f1 * f2)
rho2 = ( math.pi * w * R2 * f1 * f2 ) / ( math.log(2) )
sigma3 = G3 * math.log(2) / (math.pi * w * f1 * f2)
rho3 = ( math.pi * w * R3 * f1 * f2 ) / ( math.log(2) )
sigma4 = G4 * math.log(2) / (math.pi * w * f1 * f2)
rho4 = ( math.pi * w * R4 * f1 * f2 ) / ( math.log(2) )
sigma5 = G5 * math.log(2) / (math.pi * w * f1 * f2)
rho5 = ( math.pi * w * R5 * f1 * f2 ) / ( math.log(2) )
"""

#### CALCULO MODELO 2, amostra retangular de comprimento finito a, largura finita d e espessura w
if w < (4/10)*s:
    print('ok')
    print(d/s)
    print(a/d)

f3 = (math.pi)/((math.pi*s/d) + math.log(1 - math.exp(-4*math.pi*s/d)) - math.log(1 - math.exp(-2*math.pi*s/d)) + (math.exp(-2*math.pi*s*(a/s-2)/d)*((1 - math.exp(-6*math.pi*s/d)*(1 - math.exp(-2*math.pi*s/d))/(1 + math.exp(-2*math.pi*a/d))))))
print('f3 =', f3)

# Condutividades e Resistividades
sigma1 = G1 / (w * f3)
rho1 =  R1 * w * f3 
sigma2 = G2 / (w * f3)
rho2 = R2 * w * f3
sigma3 = G3 / (w * f3)
rho3 = R3 * w * f3
sigma4 = G4 / (w * f3)
rho4 = R4 * w * f3
sigma5 = G5 / (w * f3)
rho5 = R5 * w * f3

sigma = (sigma1+sigma2+sigma3+sigma4+sigma5)/5
rho = (rho1+rho2+rho3+rho4+rho5)/5

#desvio = (((rho1-rho)**2+(rho2-rho)**2+(rho3-rho)**2+(rho4-rho)**2+(rho5-rho)**2)*(1/2))/5
#print('desvio', desvio)
desvio = [rho1, rho2, rho3, rho4, rho5]
print('desvio =', np.std(desvio))

# condutividade literatura ~10^4
# resistividade literatura ~10^{-4}

print('condutividade', sigma, '1/Ohm*cm')
print('resistividade', rho, 'Ohm*cm')
print('Rs =', rho/w)

b = open(str('results_')+str(name)+"_"+"values.txt", "w")
b.write('sigma1 = ' + str(sigma1) + ' ' + '1/Ohm*cm' + '\n')
b.write('sigma2 = ' + str(sigma2) + ' ' + '1/Ohm*cm' + '\n')
b.write('sigma3 = ' + str(sigma3) + ' ' + '1/Ohm*cm' + '\n')
b.write('sigma4 = ' + str(sigma4) + ' ' + '1/Ohm*cm' + '\n')
b.write('sigma5 = ' + str(sigma5) + ' ' + '1/Ohm*cm' + '\n')
b.write('rho1 = ' + str(rho1) + ' ' + 'Ohm*cm' + '\n')
b.write('rho2 = ' + str(rho2) + ' ' + 'Ohm*cm' + '\n')
b.write('rho3 = ' + str(rho3) + ' ' + 'Ohm*cm' + '\n')
b.write('rho4 = ' + str(rho4) + ' ' + 'Ohm*cm' + '\n')
b.write('rho5 = ' + str(rho5) + ' ' + 'Ohm*cm' + '\n')
b.write('.......................' + ' ' + '\n')
b.write('Condutividade elétrica: sigma = ' + str(sigma) + ' ' + '1/Ohm*cm' + '\n')
b.write('Resistividade elétrica: sigma = ' + str(rho) + ' ' + 'Ohm*cm' + '\n')
b.close()
