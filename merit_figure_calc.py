# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:03:39 2021

@author: joaoi
"""

# Figura de mérito

name = 'Merit_Figure'

rho = 1.3086389155254565e-06 # [Ohm m]
S = 4.386629525869284e-06 # [V/K]
kappa = 3.104880170238993 # [W/mK]


Z = (S**2)/rho*kappa # [V^2 m K / K^2 Ohm m W] = [V^2 / K Ohm W] = [1/K]
print('merit of figure -> Z =', Z, 'K^(-1)')

b = open(str('results_')+str(name)+"_"+"values.txt", "w")
b.write('Merit Figure: Z = ' + str(Z) + ' ' + '1/K' + '\n')
b.close()

# Teorico

rho1 = 1.0e-06 # Ohm m
rho2 = 3.2e-05 # Ohm m
S1 = 5.96e-06
S2 = 43.16e-06
kappa1 = 0.84
kappa2 = 10

Z1 = (S1**2)/rho1*kappa1 # [V^2 m K / K^2 Ohm m W] = [V^2 / K Ohm W] = [1/K]
Z2 = (S2**2)/rho2*kappa2 # [V^2 m K / K^2 Ohm m W] = [V^2 / K Ohm W] = [1/K]
print(Z1, Z2)