# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:40:50 2020

@author: LAB MAt
"""

"""
Kohlrausch method for thermal conductivity
Keithley 2100i (irá medir corrente nos pontos internos da amostra)
Keithley 2400 (aplica corrente no resistor embaixo da amostra)
Keithley 2100v (irá medir tensão nos pontos externos)
Placa DAQ (caso temperaturas não estiverem corretas abrir Nidaqmx e fazer Self-calibrate)
Arduino
2 Fontes BK Precision XLN 3640
Fonte BK Precision 1786 B
"""

import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
from simple_pid import PID
import nidaqmx
from pyfirmata import Arduino

# Parâmetros da amostra
A = 1 # área transversal
L = 1 # comprimento

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
    k2400.write(":SENS:CURR:RANG 10E-2")     # 10mA measure range.
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
def K2100i():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194206::INSTR')
    k2100.write('*CLS')
    current = float(k2100.query('MEASure:CURRent:DC?'))
    print(current)
    return current

# Definida função que usará Keithley 2100 usada para medir tensão pontos externos
# keithley que está embaixo da 2400
def K2100v():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194579::INSTR')
    k2100.write('*CLS')
    voltage = float(k2100.query('MEASure:VOLTage:DC?'))
    print(voltage)
    return voltage

"""
# define função que irá ler a temperatura através da placa daq e termopares
def temperature(caminho):  
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_thrmcpl_chan(caminho)
        data = task.read()
    return np.array(data)
"""

starttime = time.time()
T9_pid = [] #termopar saída a9, frio
T10_pid = [] #termopar saída a10, centro
T11_pid = [] #termopar saída a11, quente
t = []

# Definindo parâmetros Arduino
board = Arduino("COM11") # Define a porta do Arduino no PC
pin_cold1 = board.get_pin('d:5:p') # define a porta de saída do Arduino (digital:5:pwm)
pin_cold2 = board.get_pin('d:6:p') # define a porta de saída do Arduino (digital:6:pwm)

# Função que aplica os pid
pid_cold1 = PID(0.02, 0.04, 2.5, setpoint = 10) # peltier frio 1
pid_cold2 = PID(0.02, 0.04, 2.5, setpoint = 10) # peltier frio 2
pid_hot = PID(1, 1, 1, setpoint = 40) # resistor, meio da amostra

# Armazena as tensões aplicadas pela fonte no peltier
tensao_frio1 = []
tensao_frio2 = []

tensao_quente = []

# Definindo variáveis que vão ser utilizadas na medida do coeficiente Seebeck
v = [] # tensão amostra
T9 = [] # frio
T10 = [] # medio
T11 = [] # quente
DT = [] # diferença de temperatura entre T11 e T9 na amostra

# Valor de corrente que está passando no resistor para esquentar o meio da amostra
I = []

# máxima voltagem a ser aplicada no resistor para aquecer o centro da amostra
max_voltage = 3

# valor de corrente medido atravessando a amostra
i = []

# Lê as temperaturas através placa daq e termopares
T_cold1 = temperature("Dev2/ai11") # temperatura peltier quente
T_cold2 = temperature("Dev2/ai9") # temperatura peltier frio
T_hot = temperature("Dev2/ai10") # temperatura do centro da amostra

# Variáveis usadas para controlar o tempo que serão realizadas as medidas
start_med = 0
end_med = 0

# Estabelecer temperaturas T1 e T3, frias (dois peltier com mesmo lado frio virado para cima) (ou troca os fios)

plt.ion()
for l in range(0, 5):
    control_hot = pid_hot(T_hot)
    if control_hot < 0:
        control_hot = 0
    if control_hot > max_voltage:
        control_hot = max_voltage
    tensao_quente.append(control_hot)
    
    # Como estou esfriando os dois peltier, os 2 pid estão com sinal negativo
    control1 = - pid_cold1(T_cold1) # lê a tensão que se deve aplicar calculado pela biblioteca pid para esquentar
    tensao_frio1.append(control1) # adiciona o valor de tensão aplicada no peltier quente a uma lista
    control2 = - pid_cold2(T_cold2) # lê a tensão que se deve aplicar calculado pela biblioteca pid para esfriar (por isso o sinal negativo)
    tensao_frio2.append(control2) # adiciona o valor de tensão aplicada no peltier frio a uma lista
    # transforma o valor de tensão de saída para o valor que irá ser aplicado pelo arduino, parte quente
    control1_cold1 =  7.605*(10**(-6))*(control1)**5 - 1.49632*(10**(-4))*(control1)**4 + 0.00126*(control1)**3 - 0.00302*(control1)**2 + 0.02051*(control1)-0.00201
    # transforma o valor de tensão de saída para o valor que irá ser aplicado pelo arduino, parte fria
    control2_cold2 =  7.605*(10**(-6))*(control22)**5 - 1.49632*(10**(-4))*(control2)**4 + 0.00126*(control2)**3 - 0.00302*(control2)**2 + 0.02051*(control2)-0.00201
    # se der valor negativo é pq está acima (hot) ou abaixo (cold) do desejado, como arduino não solta valores negativos, zeramos
    if control1_cold1 < 0:
        control1_cold1 = 0
    if control1_cold1 > 10:
        control1_cold1 = 10
    if control2_cold2 < 0:
        control2_cold2 = 0
    if control2_cold2 > 10:
        control2_cold2 = 10
    
    I.append(K2400(control_hot)) # I = corrente passando pelo resistor
    pin_cold1.write(control1_cold1) # aplica tensão no pino quente, arduino
    pin_cold2.write(control2_cold2) # aplica tensão no pino frio, arduino
    
    # Vai realizar as medidas de tesão e temperatura por 5 segundos
    start_med = time.time()
    while (end_med - start_med < 5):
        i.append(K2100i())
        v.append(K2100v())
        T9.append(temperature("Dev2/ai9"))
        T10.append(temperature("Dev2/ai10"))
        T11.append(temperature("Dev2/ai11"))
        end_med = time.time()
        
    with open("conductivity.txt", 'w') as cond:
            for c in range(len(v)):
                cond.write(str(v[c]) + " " + str(i[c]) + " " + str(T9[c]) + " " + str(T10[c]) + " " + str(T11[c]) + '\n')
            cond.close()
    
    board.pass_time(1) # aguarda para fazer proxima aplicação. comando necessário para não zerar a saída do arduino a cada aplicação
    
    T_cold1 = temperature("Dev2/ai11") # temperatura peltier quente
    T_cold2 = temperature("Dev2/ai9") # temperatura peltier frio
    print(T_cold1, T_cold2)
    
    t.append(time.time()- starttime)
    T9_pid.append(T_cold1)
    T10_pid.append(temperature("Dev2/ai10")) # lê temperatura do termopar do centro, referência
    T11_pid.append(T_cold2)
    
    with open ("pid_conductivity.txt", 'w') as pid:
        for p in range(len(tensao_frio1)):
            pid.write(str(t[p]) + " " + str(tensao_quente[p]) + " " + str(I[p]) + " " + str(tensao_frio1[p]) + " " + str(tensao_frio2[p]) + " " + str(T9_pid[p]) + " " + str(T10_pid[p]) + " " + str(T11_pid[p]) + '\n')
        pid.close()
    
    plt.plot(np.array(t), np.array(T9_pid), 'r',label='Frio') 
    plt.plot(np.array(t), np.array(T10_pid), 'k',label='Quente') 
    plt.plot(np.array(t), np.array(T11_pid), 'b',label='Frio')
    plt.legend()
    plt.show() # mostra o gráfico
    plt.pause(1)
    plt.clf() # limpa o gráfico anterior e vai colocando um novo a cada medida feita
# fim plot grafico
plt.ioff()

# sai da placa arduino
board.exit()
