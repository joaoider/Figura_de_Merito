# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:33:31 2020

@author: lsd_u
"""


"""
Utiliza 2 arduinos: arduino Uno ligado com sensores MAX6675 e Arduino Mega2560 para saída de tensão
        Arduino Uno ligado na porta COM4, 
        Arduino Mega2560 ligado na porta COM7
2 Fontes BK Precision XLN3640 ligadas a um filtro de tensão passa-baixa, ligado ao Arduino Mega2560
        Fonte 'de cima' ligada na saída 11 do Arduino Mega2560 e ligado no peltier quente
        Fonte 'de baixo' ligada na saída 3 do Arduino Mega2560 e ligado no peltier frio
Multímetro Keithley 2100 (Embaixo da Fonte Keithley2400)
        Ligar os dois fios dos pinos externos. 
"""


##############################################################################################################################################
#                         BIBLIOTECAS
##############################################################################################################################################

import numpy as np
from pyfirmata import Arduino
import matplotlib.pyplot as plt
import time
import pyvisa as visa
import serial

# Definindo variáveis que vão ser utilizadas na medida do coeficiente Seebeck
v = [] # tensão amostra
T9 = [] # frio
T11 = [] # quente
DT = [] # T11- T9


##############################################################################################################################################
#                    DEFININDO PARÂMETROS DA MEDIDA 
##############################################################################################################################################

# Range de tensões aplicadas
tensao_inicial = 0.1 # (0.1 é o valor mínimo para iniciar)
tensao_final = 13
passo = 0.1


##############################################################################################################################################
#                         DEFININDO FUNÇÕES     
##############################################################################################################################################

# Define porta do Arduino Uno
ser = serial.Serial('COM4') # location of arduino port

# define função que irá ler as temperaturas a partir da porta serial, dados gerados pelo programa do Arduino Uno
def temperatura():
        dados = ser.readline()
        frio = float(dados[:5].decode("utf-8"))
        # medio = float(dados[5:12].decode("utf-8"))
        quente = float(dados[5:].decode("utf-8"))
        return frio, quente

# Definindo parâmetros Arduino MEGA
board = Arduino("COM7") # Define a porta do Arduino no PC
pin_cold = board.get_pin('d:3:p') # define a porta de saída do Arduino (digital:3:pwm)
pin_hot = board.get_pin('d:11:p') # define a porta de saída do Arduino (digital:11:pwm)

# Definida função que usará Keithley 2100 usada para medir tensão nos pontos externos
def K2100():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194579::INSTR')
    k2100.write('*CLS')
    voltage = float(k2100.query('MEASure:VOLTage:DC?'))
    return voltage

# função para fazer ajuste linear
def linear(x, a, b):
    return a * x + b


##############################################################################################################################################
#                       VARIÁVEIS
##############################################################################################################################################

# Listas com valores das tensões aplicadas
tensao = np.arange(tensao_inicial, tensao_final, passo)

starttime = time.time()
t = []


##############################################################################################################################################
#                       MEDIDAS
##############################################################################################################################################

# Medidas e gráfico
plt.ion()
for i in tensao:
        controlh = 7.605*(10**(-6))*(i)**5 - 1.49632*(10**(-4))*(i)**4 + 0.00126*(i)**3 - 0.00302*(i)**2 + 0.02051*(i) - 0.00201
        controlf = 7.605*(10**(-6))*(i/4)**5 - 1.49632*(10**(-4))*(i/4)**4 + 0.00126*(i/4)**3 - 0.00302*(i/4)**2 + 0.02051*(i/4) - 0.00201
        # print(i, control)
        pin_hot.write(controlh)
        pin_cold.write(controlf)
        board.pass_time(1)
        #time.sleep(2)
        T_cold, T_hot = temperatura()
        print(T_cold, T_hot)
        T9.append(T_cold)
        T11.append(T_hot)
        DT.append(T_hot - T_cold)
        v.append(100000*K2100())
        print(100000*K2100())
        
        t.append(time.time()- starttime)
        
        # Plotando gráfico de temperatura pelo tempo para visualização da estabilidade
        #plt.plot(np.array(DT), np.array(v), 'k*')
        #plt.plot(DT, linear(DT, *popt)*1000., 'r')
        plt.plot(np.array(t), np.array(v), 'k*') 
        plt.plot(np.array(t), np.array(T9), 'b*')
        plt.plot(np.array(t), np.array(T11), 'r*')
        plt.show() # mostra o gráfico
        plt.pause(1)    
        plt.clf() # limpa o gráfico anterior e vai colocando um novo a cada medida feita
        
        with open('seebeck.txt', 'w') as seeb:
            for s in range(len(v)):
                seeb.write(str(v[s]) + " " + str(T9[s]) + " " + str(T11[s]) + '\n')
            seeb.close()
plt.ioff()

# zerar saída de tensão para encerrar o programa
pin_hot.write(0)
pin_cold.write(0)


# sai da placa arduino
board.exit()