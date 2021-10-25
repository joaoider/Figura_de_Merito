# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:26:11 2020

@author: lsd_u
"""

"""
Kohlrausch method for thermal conductivity
# (não precisa) Keithley 2100i (irá medir corrente nos pontos internos da amostra)
Keithley 2400 (aplica corrente no resistor embaixo da amostra)
Keithley 2100v (irá medir tensão nos pontos externos)
Arduino e sensores MAX6675 para medir temperatura
Arduino
2 Fontes BK Precision XLN 3640
Fonte BK Precision 1786 B
"""
##############################################################################################################################################
#                         BIBLIOTECAS
##############################################################################################################################################

import pyvisa as visa
import numpy as np
from pyfirmata import Arduino
import serial

####################################################################################################################################################################
#                         PARÂMETROS DA AMOSTRA E DA MEDIDA
#####################################################################################################################################################################

# Parâmetros da amostra
A = 1 # área transversal
L = 1 # comprimento

# Range de tensões aplicadas no Peltier
tensao_inicial = 0.1 # (0.1 é o valor mínimo para iniciar)
tensao_final = 5.
passo = 0.1

#######################################################################################################################################################################
#                        DEFININDO FUNÇÕES
#######################################################################################################################################################################
                         
# Definida função que usará Keithley 2400 usada para aplicar tensão nos dois pontos externos, de onde se lerá a corrente
def K2400(voltage):
    rm = visa.ResourceManager()
    rm.list_resources()
    k2400 = rm.open_resource('GPIB1::24::INSTR') # definindo Keithley2400
    k2400.write(":SOUR:FUNC VOLT")          # Select voltage source.
    k2400.write(":SOUR:VOLT:MODE FIXED")    # Fixed voltage source mode.
    k2400.write(":SOUR:VOLT:LEV %f" %voltage)        # Source output = 1V.
    k2400.write(":SENS:CURR:PROT 10E-1")    # 10mA compliance.
    k2400.write(":SENS:FUNC 'CURR'")        # Current measure function.
    k2400.write(":SENS:CURR:RANG 10E-1")     # 10mA measure range.
    k2400.write(":FORM:ELEM CURR")          # Current reading only.
    k2400.write(":OUTP ON")                 # Output on before measuring.
    k2400.query(":READ?")                   #coletar informação da fonte
    current1 = k2400.query_ascii_values(":FETC?")
    print(current1)
    return current1

# Keithley 2400
def reset2400():
    rm = visa.ResourceManager()
    rm.list_resources()
    k2400 = rm.open_resource('GPIB1::24::INSTR') # definindo Keithley2400
    k2400.write("*RST") # reseta Keithley2400  # Restore GPIB defaults.

# Definida função que usará Keithley 2100 usada para medir corrente entre pontos internos
# keithley que está em cima da 2400
#def K2100i():
#    rm = visa.ResourceManager()
#    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194206::INSTR')
#    k2100.write('*CLS')
#    current = float(k2100.query('MEASure:CURRent:DC?'))
#    print(current)
#    return current

# Definida função que usará Keithley 2100 usada para medir tensão pontos externos
# keithley que está embaixo da 2400
def K2100v():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194579::INSTR')
    k2100.write('*CLS')
    voltage = float(k2100.query('MEASure:VOLTage:DC?'))
    print(voltage)
    return voltage

# Temperatura
ser = serial.Serial('COM4') # location of arduino port
# define função que irá ler as temperaturas a partir da porta serial, dados gerados pelo programa do Arduino
def temperatura():
        dados = ser.readline()
        frio1 = float(dados[:5].decode("utf-8"))
        medio = float(dados[5:12].decode("utf-8"))
        frio2 = float(dados[14:].decode("utf-8"))
        return frio1, medio, frio2

# Definindo parâmetros Arduino MEGA
board = Arduino("COM7") # Define a porta do Arduino no PC
pin_cold1 = board.get_pin('d:3:p') # define a porta de saída do Arduino (digital:3:pwm)
pin_cold2 = board.get_pin('d:11:p') # define a porta de saída do Arduino (digital:11:pwm)

########################################################################################################################################################################
#                        VARIÁVEIS
#########################################################################################################################################################################

# Listas com valores das tensões aplicadas no peltier
tensao = np.arange(tensao_inicial, tensao_final, passo)

T9 = []
T10 = []
T11 = []
v = []
#I = []

############################################################################################################################################################################
#                        MEDIDAS
###########################################################################################################################################################################
for i in tensao:
        control = 7.605*(10**(-6))*(i)**5 - 1.49632*(10**(-4))*(i)**4 + 0.00126*(i)**3 - 0.00302*(i)**2 + 0.02051*(i) - 0.00201
        # print(i, control)
        pin_cold1.write(control)
        pin_cold2.write(control)
        board.pass_time(3)
        K2400(10)
        T_cold1, T_medio, T_cold2 = temperatura()
        print(T_cold1, T_medio, T_cold2)
        T9.append(T_cold1)
        T10.append(T_medio)
        T11.append(T_cold2)
        #I.append(K2100i())
        v.append(K2100v())
        
        with open('thermal.txt', 'w') as therm:
            for t in range(len(v)):
                therm.write(str(T9[t]) + " " + str(T10[t]) + " " + str(T11[t]) +  " " + str(v[t]) + '\n')
            therm.close()

# zera saída de tensão para encerrar programa
pin_cold1.write(0)
pin_cold2.write(0)

#zera a saída de tensão 
K2400(0)

# sai da placa arduino
board.exit()

# condutividade térmica
#k = L*I*v/(4*A(2*T_medio-(T_cold1+T_cold2)))
                        