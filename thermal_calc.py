# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:23:53 2021

@author: joaoi
"""
import numpy as np

#0.07573598011598845

# condutividade elétrica
# pegar resultado da curva IV
#sigma = 76415.29501520896

name = 'thermal'

#sigma = 76415.29501520896 # 1/Ohm*cm
sigma = 7641529.501520895 # 1/Ohm*m

name6 = 'thermal6'
# carrega dados experimentais do arquivo txt
data6 = np.loadtxt(name6+'.txt', comments='#')
T16  = data6[:,0]   # coluna 1 - temperature 1
T26  = data6[:,1]   # coluna 2 - temperature meio
T36  = data6[:,2]   # coluna 3 - temperature 3
current6  = data6[:,3]   # coluna 4 - current
voltage6 = data6[:,4]  # coluna 5 - voltage


name7 = 'thermal7'
# carrega dados experimentais do arquivo txt
data7 = np.loadtxt(name7+'.txt', comments='#')
T17  = data7[:,0]   # coluna 1 - temperature 1
T27  = data7[:,1]   # coluna 2 - temperature meio
T37  = data7[:,2]   # coluna 3 - temperature 3
current7  = data7[:,3]   # coluna 4 - current
voltage7 = data7[:,4]  # coluna 5 - voltage

name8 = 'thermal8'
# carrega dados experimentais do arquivo txt
data8 = np.loadtxt(name8+'.txt', comments='#')
T18  = data8[:,0]   # coluna 1 - temperature 1
T28  = data8[:,1]   # coluna 2 - temperature meio
T38  = data8[:,2]   # coluna 3 - temperature 3
current8  = data8[:,3]   # coluna 4 - current
voltage8 = data8[:,4]  # coluna 5 - voltage

name9 = 'thermal9'
# carrega dados experimentais do arquivo txt
data9 = np.loadtxt(name9+'.txt', comments='#')
T19  = data9[:,0]   # coluna 1 - temperature 1
T29  = data9[:,1]   # coluna 2 - temperature meio
T39  = data9[:,2]   # coluna 3 - temperature 3
current9  = data9[:,3]   # coluna 4 - current
voltage9 = data9[:,4]  # coluna 5 - voltage

name10 = 'thermal10'
# carrega dados experimentais do arquivo txt
data10 = np.loadtxt(name10+'.txt', comments='#')
T110  = data10[:,0]   # coluna 1 - temperature 1
T210  = data10[:,1]   # coluna 2 - temperature meio
T310  = data10[:,2]   # coluna 3 - temperature 3
current10  = data10[:,3]   # coluna 4 - current
voltage10 = data10[:,4]  # coluna 5 - voltage

name11 = 'thermal11'
# carrega dados experimentais do arquivo txt
data11 = np.loadtxt(name11+'.txt', comments='#')
T111  = data11[:,0]   # coluna 1 - temperature 1
T211  = data11[:,1]   # coluna 2 - temperature meio
T311  = data11[:,2]   # coluna 3 - temperature 3
current11  = data11[:,3]   # coluna 4 - current
voltage11 = data11[:,4]  # coluna 5 - voltage

name12 = 'thermal12'
# carrega dados experimentais do arquivo txt
data12 = np.loadtxt(name12+'.txt', comments='#')
T112  = data12[:,0]   # coluna 1 - temperature 1
T212  = data12[:,1]   # coluna 2 - temperature meio
T312  = data12[:,2]   # coluna 3 - temperature 3
current12  = data12[:,3]   # coluna 4 - current
voltage12 = data12[:,4]  # coluna 5 - voltage

name13 = 'thermal13'
# carrega dados experimentais do arquivo txt
data13 = np.loadtxt(name13+'.txt', comments='#')
T113  = data13[:,0]   # coluna 1 - temperature 1
T213  = data13[:,1]   # coluna 2 - temperature meio
T313  = data13[:,2]   # coluna 3 - temperature 3
current13  = data13[:,3]   # coluna 4 - current
voltage13 = data13[:,4]  # coluna 5 - voltage

name14 = 'thermal14'
# carrega dados experimentais do arquivo txt
data14 = np.loadtxt(name14+'.txt', comments='#')
T114  = data14[:,0]   # coluna 1 - temperature 1
T214  = data14[:,1]   # coluna 2 - temperature meio
T314  = data14[:,2]   # coluna 3 - temperature 3
current14  = data14[:,3]   # coluna 4 - current
voltage14 = data14[:,4]  # coluna 5 - voltage

# calcula media da temperatura entre as pontas
Tmedio6 = []
for i in range (len(T16)):
    Tmedio6.append((T16[i]+T36[i])/2)
Tmedio7 = []
for i in range (len(T17)):
    Tmedio7.append((T17[i]+T37[i])/2)
Tmedio8 = []
for i in range (len(T18)):
    Tmedio8.append((T18[i]+T38[i])/2)
Tmedio9 = []
for i in range (len(T19)):
    Tmedio9.append((T19[i]+T39[i])/2)
Tmedio10 = []
for i in range (len(T110)):
    Tmedio10.append((T110[i]+T310[i])/2)
Tmedio11 = []
for i in range (len(T111)):
    Tmedio11.append((T111[i]+T311[i])/2)
Tmedio12 = []
for i in range (len(T112)):
    Tmedio12.append((T112[i]+T312[i])/2)
Tmedio13 = []
for i in range (len(T113)):
    Tmedio13.append((T113[i]+T313[i])/2)
Tmedio14 = []
for i in range (len(T114)):
    Tmedio14.append((T114[i]+T314[i])/2)

# condutividade térmica
kappa6 = []
for j in range (len(T16)):
    kappa6.append(sigma*(voltage6[j]**2)/(8*(T26[j]-Tmedio6[j])))
kappa7 = []
for j in range (len(T17)):
    kappa7.append(sigma*(voltage7[j]**2)/(8*(T27[j]-Tmedio7[j])))
kappa8 = []
for j in range (len(T18)):
    kappa8.append(sigma*(voltage8[j]**2)/(8*(T28[j]-Tmedio8[j])))
kappa9 = []
for j in range (len(T19)):
    kappa9.append(sigma*(voltage9[j]**2)/(8*(T29[j]-Tmedio9[j])))
kappa10 = []
for j in range (len(T110)):
    kappa10.append(sigma*(voltage10[j]**2)/(8*(T210[j]-Tmedio10[j])))
kappa11 = []
for j in range (len(T111)):
    kappa11.append(sigma*(voltage11[j]**2)/(8*(T211[j]-Tmedio11[j])))
kappa12 = []
for j in range (len(T112)):
    kappa12.append(sigma*(voltage12[j]**2)/(8*(T212[j]-Tmedio12[j])))
kappa13 = []
for j in range (len(T113)):
    kappa13.append(sigma*(voltage13[j]**2)/(8*(T213[j]-Tmedio13[j])))
kappa14 = []
for j in range (len(T114)):
    kappa14.append(sigma*(voltage14[j]**2)/(8*(T214[j]-Tmedio14[j])))
    
# calculando condutividade termica media dos valores pra cada medida
kappa_f6 = sum(kappa6)/len(kappa6)
kappa_f7 = sum(kappa7)/len(kappa7)
kappa_f8 = sum(kappa8)/len(kappa8)
kappa_f9 = sum(kappa9)/len(kappa9)
kappa_f10 = sum(kappa10)/len(kappa10)
kappa_f11= sum(kappa11)/len(kappa11)
kappa_f12 = sum(kappa12)/len(kappa12)
kappa_f13 = sum(kappa13)/len(kappa13)
kappa_f14 = sum(kappa14)/len(kappa14)

######################################################
name100 = 'thermal100'
# carrega dados experimentais do arquivo txt
dataa = np.loadtxt(name100+'.txt', comments='#')
Ta1  = dataa[:,0]   # coluna 1 - temperature 1
Ta2  = dataa[:,1]   # coluna 2 - temperature meio
Ta3  = dataa[:,2]   # coluna 3 - temperature 3
#currenta  = dataa[:,3]   # coluna 4 - current
voltagea = dataa[:,3]  # coluna 5 - voltage

Tmedioa = []
for i in range (len(Ta1)):
    Tmedioa.append((Ta1[i]+Ta3[i])/2)

kappaa = []
for j in range (len(Ta1)):
    kappaa.append(sigma*(voltagea[j]**2)/(8*(Ta2[j]-Tmedioa[j])))
    
kappa_fa = sum(kappaa)/len(kappaa)
###############################################################
name101 = 'thermal101'
# carrega dados experimentais do arquivo txt
datab = np.loadtxt(name101+'.txt', comments='#')
Tb1  = datab[:,0]   # coluna 1 - temperature 1
Tb2  = datab[:,1]   # coluna 2 - temperature meio
Tb3  = datab[:,2]   # coluna 3 - temperature 3
#currenta  = dataa[:,3]   # coluna 4 - current
voltageb = datab[:,3]  # coluna 5 - voltage

Tmediob = []
for i in range (len(Tb1)):
    Tmediob.append((Tb1[i]+Tb3[i])/2)

kappab = []
for j in range (len(Tb1)):
    kappab.append(sigma*(voltageb[j]**2)/(8*(Tb2[j]-Tmediob[j])))
    
kappa_fb = sum(kappab)/len(kappab)
###############################################################

# condutividade termica geral
kappa_f = (kappa_f10 + kappa_f11 + kappa_f12 + kappa_f13 + kappa_f14)/5
print(kappa_f)
desvio = [kappa_f10, kappa_f11, kappa_f12, kappa_f13, kappa_f14]
print('desvio', np.std(desvio))

b = open(str('results_')+str(name)+"_"+"values.txt", "w")
b.write('kappa6 = ' + str(kappa_f6) + ' ' + 'W/mK' + '\n')
b.write('kappa7 = ' + str(kappa_f7) + ' ' + 'W/mK' + '\n')
b.write('kappa8 = ' + str(kappa_f8) + ' ' + 'W/mK' + '\n')
b.write('kappa9 = ' + str(kappa_f9) + ' ' + 'W/mK' + '\n')
b.write('kappa10 = ' + str(kappa_f10) + ' ' + 'W/mK' + '\n')
b.write('kappa11 = ' + str(kappa_f11) + ' ' + 'W/mK' + '\n')
b.write('kappa12 = ' + str(kappa_f12) + ' ' + 'W/mK' + '\n')
b.write('kappa13 = ' + str(kappa_f13) + ' ' + 'W/mK' + '\n')
b.write('kappa14 = ' + str(kappa_f14) + ' ' + 'W/mK' + '\n')
b.write('kappaa = ' + str(kappa_fa) + ' ' + 'W/mK' + '\n')
b.write('kappab = ' + str(kappa_fb) + ' ' + 'W/mK' + '\n')
b.write('.......................' + ' ' + '\n')
#b.write('Média das 5 melhores medidas: kappa 6, 8, 9, 10 e 13' + ' ' + '\n')
b.write('Condutividade térmica: kappa = ' + str(kappa_f) + ' ' + 'W/mK' + '\n')
b.write('Desvio: ' + str(np.std(desvio)) + ' ' + 'W/mK' + '\n')
b.close()