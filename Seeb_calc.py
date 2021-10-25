# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Calculo da resistividade e condutividade eletrica

import math
import numpy as np
import math
from scipy.optimize import curve_fit

name = 'Seebeck'

name4 = 'seebeck4'
# carrega dados experimentais do arquivo txt
data4 = np.loadtxt(name4+'.txt', comments='#')
voltage4 = data4[:,0]   # coluna 1 - voltage
voltagef4 = []
for i in range(len(voltage4)):
    voltagef4.append(voltage4[i]/100000)
temperature14 = data4[:,1]  # coluna 2 - temperature cold
temperature24 = data4[:,2]  # coluna 3 - temperature hot
DT4 = []
for i in range(len(temperature14)):
    DT4.append(temperature24[i]-temperature14[i])

name5 = 'seebeck5'
# carrega dados experimentais do arquivo txt
data5 = np.loadtxt(name5+'.txt', comments='#')
voltage5 = data5[:,0]   # coluna 1 - voltage
voltagef5 = []
for i in range(len(voltage5)):
    voltagef5.append(voltage5[i]/100000)
temperature15 = data5[:,1]  # coluna 2 - temperature cold
temperature25 = data5[:,2]  # coluna 3 - temperature hot
DT5 = []
for i in range(len(temperature15)):
    DT5.append(temperature25[i]-temperature15[i])

name6 = 'seebeck6'
# carrega dados experimentais do arquivo txt
data6 = np.loadtxt(name6+'.txt', comments='#')
voltage6 = data6[:,0]   # coluna 1 - voltage
voltagef6 = []
for i in range(len(voltage6)):
    voltagef6.append(voltage6[i]/100000)
temperature16 = data6[:,1]  # coluna 2 - temperature cold
temperature26 = data6[:,2]  # coluna 3 - temperature hot
DT6 = []
for i in range(len(temperature16)):
    DT6.append(temperature26[i]-temperature16[i])
    
name7 = 'seebeck7'
# carrega dados experimentais do arquivo txt
data7 = np.loadtxt(name7+'.txt', comments='#')
voltage7 = data7[:,0]   # coluna 1 - voltage
voltagef7 = []
for i in range(len(voltage7)):
    voltagef7.append(voltage7[i]/100000)
temperature17 = data7[:,1]  # coluna 2 - temperature cold
temperature27 = data7[:,2]  # coluna 3 - temperature hot
DT7 = []
for i in range(len(temperature17)):
    DT7.append(temperature27[i]-temperature17[i])
    
name8 = 'seebeck8'
# carrega dados experimentais do arquivo txt
data8 = np.loadtxt(name8+'.txt', comments='#')
voltage8 = data8[:,0]   # coluna 1 - voltage
voltagef8 = []
for i in range(len(voltage8)):
    voltagef8.append(voltage8[i]/100000)
temperature18 = data8[:,1]  # coluna 2 - temperature cold
temperature28 = data8[:,2]  # coluna 3 - temperature hot
DT8 = []
for i in range(len(temperature18)):
    DT8.append(temperature28[i]-temperature18[i])
    
name9 = 'seebeck9'
# carrega dados experimentais do arquivo txt
data9 = np.loadtxt(name9+'.txt', comments='#')
voltage9 = data9[:,0]   # coluna 1 - voltage
voltagef9 = []
for i in range(len(voltage9)):
    voltagef9.append(voltage9[i]/100000)
temperature19 = data9[:,1]  # coluna 2 - temperature cold
temperature29 = data9[:,2]  # coluna 3 - temperature hot
DT9 = []
for i in range(len(temperature19)):
    DT9.append(temperature29[i]-temperature19[i])
    
name10 = 'seebeck10'
# carrega dados experimentais do arquivo txt
data10 = np.loadtxt(name10+'.txt', comments='#')
voltage10 = data10[:,0]   # coluna 1 - voltage
voltagef10 = []
for i in range(len(voltage10)):
    voltagef10.append(voltage10[i]/100000)
temperature110 = data10[:,1]  # coluna 2 - temperature cold
temperature210 = data10[:,2]  # coluna 3 - temperature hot
DT10 = []
for i in range(len(temperature110)):
    DT10.append(temperature210[i]-temperature110[i])
    
name11 = 'seebeck11'
# carrega dados experimentais do arquivo txt
data11 = np.loadtxt(name11+'.txt', comments='#')
voltage11 = data11[:,0]   # coluna 1 - voltage
voltagef11 = []
for i in range(len(voltage11)):
    voltagef11.append(voltage11[i]/100000)
temperature111 = data11[:,1]  # coluna 2 - temperature cold
temperature211 = data11[:,2]  # coluna 3 - temperature hot
DT11 = []
for i in range(len(temperature111)):
    DT11.append(temperature211[i]-temperature111[i])
    
name12 = 'seebeck12'
# carrega dados experimentais do arquivo txt
data12 = np.loadtxt(name12+'.txt', comments='#')
voltage12 = data12[:,0]   # coluna 1 - voltage
voltagef12 = []
for i in range(len(voltage12)):
    voltagef12.append(voltage12[i]/100000)
temperature121 = data12[:,1]  # coluna 2 - temperature cold
temperature212 = data12[:,2]  # coluna 3 - temperature hot
DT12 = []
for i in range(len(temperature121)):
    DT12.append(temperature212[i]-temperature121[i])
    
name13 = 'seebeck13'
# carrega dados experimentais do arquivo txt
data13 = np.loadtxt(name13+'.txt', comments='#')
voltage13 = data13[:,0]   # coluna 1 - voltage
voltagef13 = []
for i in range(len(voltage13)):
    voltagef13.append(voltage13[i]/100000)
temperature131 = data13[:,1]  # coluna 2 - temperature cold
temperature213 = data13[:,2]  # coluna 3 - temperature hot
DT13 = []
for i in range(len(temperature131)):
    DT13.append(temperature213[i]-temperature131[i])

def linear(x, a, b):
    return a * x + b

# Ajuste linear
popt4, pcov4 = curve_fit(linear, DT4, voltagef4)
popt5, pcov5 = curve_fit(linear, DT5, voltagef5)
popt6, pcov6 = curve_fit(linear, DT6, voltagef6)
popt7, pcov7 = curve_fit(linear, DT7, voltagef7)
popt8, pcov8 = curve_fit(linear, DT8, voltagef8)
popt9, pcov9 = curve_fit(linear, DT9, voltagef9)
popt10, pcov10 = curve_fit(linear, DT10, voltagef10)
popt11, pcov11 = curve_fit(linear, DT11, voltagef11)
popt12, pcov12 = curve_fit(linear, DT12, voltagef12)
popt13, pcov13 = curve_fit(linear, DT13, voltagef13)


# Calculando coeficiente Seebeck
S4 = popt4[0]
S5 = popt5[0]
S6 = popt6[0]
S7 = popt7[0]
S8 = popt8[0]
S9 = popt9[0]
S10 = popt10[0]
S11 = popt11[0]
S12 = popt12[0]
S13 = popt13[0]


Seebeck = (S4 + S5 + S6 + S7 + S8 + S9 + S10 + S11 + S12 + S13)/10
print(Seebeck)
desvio = [S4, S5, S6, S7, S8, S9, S10, S11, S12, S13]
print('desvio', np.std(desvio))

# condutividade literatura ~10^4
# resistividade literatura ~10^{-4}

b = open(str('results_')+str(name)+"_"+"values.txt", "w")
b.write('Seebeck4 = ' + str(S4) + ' ' + 'V/K' + '\n')
b.write('Seebeck5 = ' + str(S5) + ' ' + 'V/K' + '\n')
b.write('Seebeck6 = ' + str(S6) + ' ' + 'V/K' + '\n')
b.write('Seebeck7 = ' + str(S7) + ' ' + 'V/K' + '\n')
b.write('Seebeck8 = ' + str(S8) + ' ' + 'V/K' + '\n')
b.write('Seebeck9 = ' + str(S9) + ' ' + 'V/K' + '\n')
b.write('Seebeck10 = ' + str(S10) + ' ' + 'V/K' + '\n')
b.write('Seebeck11 = ' + str(S11) + ' ' + 'V/K' + '\n')
b.write('Seebeck12 = ' + str(S12) + ' ' + 'V/K' + '\n')
b.write('Seebeck13 = ' + str(S13) + ' ' + 'V/K' + '\n')
b.write('.......................' + ' ' + '\n')
b.write('Coeficiente Seebeck: S = ' + str(Seebeck) + ' ' + 'V/K' + '\n')
b.close()