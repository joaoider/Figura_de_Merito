# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:42:28 2020

@author: LAB MAt
"""

"""
PROGRAMA PID, 
ARDUINO UNO, (ler temperaturas, sensor max6675)
ARDUINO MEGA, (aplicar tensões)
2 FONTES BKPRECISION XLN3640, 
2 PELTIER, 
FONTE BK PRECISION 1786B, 
Keithley 2100.(pontos externos)
"""

from simple_pid import PID
# import nidaqmx
import numpy as np
from pyfirmata import Arduino
import matplotlib.pyplot as plt
import time
import pyvisa as visa
from scipy.optimize import curve_fit
import serial

ser = serial.Serial('COM4') # location of arduino port
# - see Tools->Serial Port ->/dev/ttyACM0 or whatever yours may say

starttime = time.time()
T9_pid = [] #termopar saídas 2,3,4, frio
T10_pid = [] #termopar saídas 8,9,10 centro
T11_pid = [] #termopar saídas 11,12,13 quente
t = []
"""
# define função que irá ler a temperatura através da placa daq e termopares
def temperature(caminho):  
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_thrmcpl_chan(caminho)
        data = task.read()
    return np.array(data)
"""
# define função que irá ler as temperaturas a partir da porta serial, dados gerados pelo programa do Arduino
def temperatura():
        dados = ser.readline()
        frio = float(dados[:6].decode("utf-8"))
        medio = float(dados[9:15].decode("utf-8"))
        quente = float(dados[18:].decode("utf-8"))
        return frio, medio, quente

# Definida função que usará Keithley 2100 usada para medir tensão nos pontos externos
def K2100():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194579::INSTR')
    k2100.write('*CLS')
    voltage = float(k2100.query('MEASure:VOLTage:DC?'))
    return voltage

# Definindo variáveis que vão ser utilizadas na medida do coeficiente Seebeck
v = [] # tensão amostra
T9 = [] # frio
T10 = [] # medio
T11 = [] # quente
DT = [] # diferença de temperatura entre T11 e T9 na amostra

# Definindo parâmetros Arduino UNO para medidas de temperatura
board = Arduino("COM5") # Define a porta do Arduino no PC
pin_cold = board.get_pin('d:3:p') # define a porta de saída do Arduino (digital:3:pwm)
pin_hot = board.get_pin('d:11:p') # define a porta de saída do Arduino (digital:11:pwm)

# chama a funcao pid (proporcional, integral, derivada, valor a ser alcançado)
pid_cold = PID(0.02, 0.04, 2.5, setpoint = 5) # peltier frio
pid_hot = PID(0.02, 0.04, 2.5, setpoint = 55) # peltier quente

# Lê as temperaturas através do arduino e termopares
T_cold, T, T_hot = temperatura()

# Listas para salvar os valores das tensões aplicadas
tensao_frio = [] # lista de valores da tensão aplicada no peltier frio
tensao_quente = [] # lista de valores da tensão aplicada no peltier quente

# Lista para salvar os valores das temperaturas medidas no processo do pid
T_cold_pid = [] # valor da temperatura no peltier frio
T_hot_pid = [] # valor da temperatura no peltier quente

# Variáveis usadas para controlar o tempo que serão realizadas as medidas
start_med = 0
end_med = 0

# Inicio plot grafico
#plt.ion()
for i in range(0, 30):
    control = pid_hot(T_hot) # lê a tensão que se deve aplicar calculado pela biblioteca pid para esquentar
    tensao_quente.append(control) # adiciona o valor de tensão aplicada no peltier quente a uma lista
    control1 = - pid_cold(T_cold) # lê a tensão que se deve aplicar calculado pela biblioteca pid para esfriar (por isso o sinal negativo)
    tensao_frio.append(control1) # adiciona o valor de tensão aplicada no peltier frio a uma lista
    # transforma o valor de tensão de saída para o valor que irá ser aplicado pelo arduino, parte quente
    control_hot =  7.605*(10**(-6))*(control)**5 - 1.49632*(10**(-4))*(control)**4 + 0.00126*(control)**3 - 0.00302*(control)**2 + 0.02051*(control)-0.00201
    # transforma o valor de tensão de saída para o valor que irá ser aplicado pelo arduino, parte fria
    control_cold =  7.605*(10**(-6))*(control1)**5 - 1.49632*(10**(-4))*(control1)**4 + 0.00126*(control1)**3 - 0.00302*(control1)**2 + 0.02051*(control1)-0.00201
    # se der valor negativo é pq está acima (hot) ou abaixo (cold) do desejado, como arduino não solta valores negativos, zeramos
    if control_hot < 0:
        control_hot = 0
    if control_hot > 10:
        control_hot = 10
    if control_cold < 0:
        control_cold = 0
    if control_cold > 10:
        control_cold = 10

    pin_hot.write(control_hot) # aplica tensão no pino quente, arduino
    pin_cold.write(control_cold) # aplica tensão no pino frio, arduino
    
    # Vai realizar as medidas de tesão e temperatura por 5 segundos
    start_med = time.time()
    while (end_med - start_med < 5):
        v.append(K2100())
        T_cold, T, T_hot  = temperatura() 
        T9.append(T_cold)
        T10.append(T)
        T11.append(T_hot)
        end_med = time.time()
    # salvando dados das medidas em um aquivo txt    
    with open('seebeck.txt', 'w') as seeb:
            for s in range(len(v)):
                seeb.write(str(v[s]) + " " + str(T9[s]) + " " + str(T10[s]) + " " + str(T11[s]) + '\n')
            seeb.close()
                
    board.pass_time(1) # aguarda para fazer proxima aplicação. comando necessário para não zerar a saída do arduino a cada aplicação
    T_cold, T, T_hot  = temperatura() 
#    T_cold = temperature("Dev2/ai9") # lê temperatura fria atraves dos termopares e placa daq
#    T_hot = temperature("Dev2/ai11") # lê temperatura quente atraves dos termopares e placa daq
    print(T_cold, T_hot)
    
    # Adicionando valores de tempo e temperatura às listas para plotagem dos gráficos
    t.append(time.time()- starttime)
    T9_pid.append(T_cold)
    T10_pid.append(T) # lê temperatura do termopar do centro, referência
    T11_pid.append(T_hot)

    # Salvando dados de tensão aplicada no peltier,  temperatura e tempo
    with open ("pid_seebeck.txt", 'w') as pid:
        for p in range(len(tensao_quente)):
            pid.write(str(t[p])+ " " + str(tensao_quente[p]) + " " + str(tensao_frio[p]) + " " + str(T9_pid[p]) + " " + str(T10_pid[p]) + " " + str(T11_pid[p]) + '\n')
        pid.close()
    """
    # Plotando gráfico de temperatura pelo tempo para visualização da estabilidade
    plt.plot(np.array(t), np.array(T9_pid), 'r',label='Frio') 
    plt.plot(np.array(t), np.array(T10_pid), 'k',label='Meio') 
    plt.plot(np.array(t), np.array(T11_pid), 'b',label='Quente') 
    plt.legend()
    plt.show() # mostra o gráfico
    plt.pause(1)
    plt.clf() # limpa o gráfico anterior e vai colocando um novo a cada medida feita
    """
for i in range(0, len(T9)):
    DT.append(T11[i] - T9[i])

DT = np.array(DT)
v = np.array(v)

# fim plot grafico
#plt.ioff()

def  linear(x, a, b):
    return a * x + b

popt, pcov = curve_fit(linear, DT, v)

# Plotando gráfico de Tensão por Variação de temperatura na amostra
plt.plot(DT, v, 'k*')
plt.plot(DT, linear(DT, *popt), 'r')
plt.ylabel("V (V)")
plt.xlabel("DT (C)")
plt.title('Tensão por Temperatura')
plt.show()

# sai da placa arduino
board.exit()