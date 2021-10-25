# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:20:41 2019

@author: LAB MAt
"""

"""
############## FAZENDO CURVA IV COM TÉCNICA DE 4 PONTAS ###########
Aplica uma tensão com a Keithley 2400 nos dois pontos externos, de onde se lê a corrente.
Lê a tensão com a Keithley 2100 nos dois pontos internos.
Utiliza Arduino Uno com sensores MAX6675 para medição de temperaturas.
"""

##############################################################################################################################################
#                         BIBLIOTECAS
##############################################################################################################################################

import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import serial
#import nidaqmx


##############################################################################################################################################
#                    DEFININDO PARÂMETROS DA MEDIDA 
##############################################################################################################################################

n_medidas = 10   # número de medidas feitas em cada ponto para se tomar a média (Filtro da tensão)
tensao_inicial = -5.
tensao_final = 5.
passo = 0.1  # passo da tensão indo pra tensão inicial até tensão final
n_passos = int((tensao_final - tensao_inicial) / passo+1) # calcula o número de passos necessários pra chegar da tensão inical até a final, dado o passo
print("Número de passos: %.2f" % n_passos)


##############################################################################################################################################
#                       VARIÁVEIS
##############################################################################################################################################
       
# Variáveis, cria listas
v = [] # tensão entre os dois pontos internos
I = [] # corrente medida entre os pontos externos
T9 = [] # temperatura (lado esquerdo)
T10 = [] # temperatura centro
T11 = [] # temperatura (lado direito)
DT = [] # diferente de temperatura entre T11 e T9

t = np.linspace(tensao_inicial, tensao_final, n_passos)   # faixa de tensão aplicada

v_med = np.zeros(n_medidas)
T9_med = np.zeros(n_medidas)
T10_med = np.zeros(n_medidas)
T11_med = np.zeros(n_medidas)


##############################################################################################################################################
#                    DEFININDO PARÂMETROS DA AMOSTRA
##############################################################################################################################################

# Se a amostra for circular, colocar "c" e se for retangular, colocar "r"
# amostra = 1 é representa uma amostra circular
# amostra = 2 representa uma amostra retangular
amostra = 2
# Se o substrato da amostra for isolante colocar "i" e se for condutor colocar "c"
# substrato = 1 representa um substrato isolante
# substrato = 2 representa um substrato condutor
substrato = 1

# ESPESSURA "w", ESPAÇAMENTO ENTRE OS 4 PONTOS "s", DIÂMETRO circular "d", COMPRIMENTO retangular "c" e LARGURA retangular "l"
w = 0.018 # espessura da amostra
s = 0.003 # espaçamento entre os 4 pontos de medida
d = 1. # diâmetro da amostra circular
c = 1. # comprimento da amostra retangular (na direção dos 4 pontos)
l = 1. # largura da amostra retangular (perpendicular aos 4 pontos)


##############################################################################################################################################
#                         DEFININDO FUNÇÕES     
##############################################################################################################################################

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
    current = k2400.query_ascii_values(":FETC?")
    print(current)
    return current

# Define função para reiniciar Keithley 2400, passo necessário
def reset2400():
    rm = visa.ResourceManager()
    rm.list_resources()
    k2400 = rm.open_resource('GPIB1::24::INSTR') # definindo Keithley2400
    k2400.write("*RST") # reseta Keithley2400  # Restore GPIB defaults.

# Definida função que usará Keithley 2100 usada para medir tensão
def K2100():
    rm = visa.ResourceManager()
    k2100 = rm.open_resource('USB0::0x05E6::0x2100::1194579::INSTR')
    k2100.write('*CLS')
    voltage = float(k2100.query('MEASure:VOLTage:DC?'))
    print(voltage)
    return voltage

# ser = serial.Serial('COM4') # location of arduino port

# define função que irá ler as temperaturas a partir da porta serial, dados gerados pelo programa do Arduino
def temperatura():
        dados = ser.readline()
        frio = float(dados[:5].decode("utf-8"))
        # medio = float(dados[5:12].decode("utf-8"))
        quente = float(dados[5:].decode("utf-8"))
        return frio, quente

"""
# define função que irá ler a temperatura através da placa daq e termopares
def temperature(caminho):  
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_thrmcpl_chan(caminho)
        data = task.read()
    return np.array(data)
"""

def linear(x, a, b):
    return a * x + b


##############################################################################################################################################
#                       MEDIDAS
##############################################################################################################################################

# Realiza medidas
for i in range(0, len(t)): # varia tensão de tensao_inicial ate tensao_final com n_passos
    I.append(K2400(t[i])) # utiliza a funcao que aplica tensao e retorna o valor de corrente, acrescido na lista de I
    time.sleep(1)

    for ii in range(0, n_medidas):
        v_med[ii] = K2100() # realiza as medidas de tensao nos pontos internos
    #T_cold, T_hot = temperatura()
    #print(T_cold, T_hot)
    #T9.append(T_cold)
    #T11.append(T_hot)
    #T9.append(temperature("Dev2/ai9"))
    #T10.append(temperature("Dev2/ai10"))
    #T11.append(temperature("Dev2/ai11"))
    #print(temperature("Dev2/ai9"), temperature("Dev2/ai11"))
    v.append(np.mean(v_med))

#for i in range(0, len(T9)):
#    DT.append(T11[i] - T9[i])

# transforma as listas em vetores
v = np.array(v) 
I = np.array(I)
I = I.T[0] # transpõe a matriz

T9 = np.array(T9)
T10 = np.array(T10)
T11 = np.array(T11)
DT = np.array(DT)

print(v)
print(I)

#salva os dados em um arquivo txt
salvar = np.zeros((len(v), 2))
salvar[0:len(v),0] = v
salvar[0:len(I),1] = I
#salvar[0:len(T9),2] = T9
#salvar[0:len(T10),3] = T10
#salvar[0:len(T11),4] = T11
#salvar[0:len(T11),5] = DT
nome = 'IV_curve'
np.savetxt(nome + '.txt', salvar, header='V I')


##############################################################################################################################################
#                         GRÁFICO
##############################################################################################################################################

# Plota o gráfico
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
popt, pcov = curve_fit(linear, v, I)

# Dados para cada subplot
# Curva I-V
ax1.plot(v, I*1000., 'k*')
ax1.plot(v, linear(v, *popt)*1000., 'r')
ax1.set(title="IV Curve", xlabel="V (V)", ylabel="I (mA)")
# Curva I-DT
ax2.plot(DT, I*1000., 'k*')
ax2.set(title="Temperatura por Corrente", xlabel="I(mA)", ylabel="Gradiente Temperatura (C)")

plt.show()


##############################################################################################################################################
#                             CÁLCULOS
##############################################################################################################################################

R = 1./popt[0]
print(R)
G = float(1/R)
print("A resistência elétrica é", R, "ohms")
print("A condutâcia elétrica é", G, "siemens")

# Calculando condutividade elétrica da Amostra
""" Correções """
# f1 fator de correção de espessura
# f11 correção se o substrato for isolante
f11 = float((math.log(2))/(math.log((math.sinh(w/s)/(math.sinh(w/2*s))))))
# f12 correção se o substrat for condutor
f12 = float((math.log(2))/(math.log((math.cosh(w/s)/(math.cosh(w/2*s))))))
# f2 fator de correção de largura
# f2c corrige amostra circular e f2r amostra retangular
# No caso de d/s ou l/s >> 1 usamos essas aproximações          ### FAZER A ANÁLISE PARA TER UMA FÓRMULA GERAL !!!
f2c = f2r = 1 
# f21 correção se a amostra for circular com diâmetro d
f21 = float(f2c*(d/s)) 
# f22 correção se a amostra for retangular com largura d e comprimento a
f22 = float(f2r*(c/l,l/s))

# Condutividade
if amostra == 1: # circular
    if substrato == 1: # isolante
        sigma = float((G*math.log(2))/(f11*f21*w*math.pi)) # condutividade elétrica
        print("A Condutividade elétrica é", sigma, "(Ωm)-¹")
    if substrato == 2: # condutor
        sigma = float((G*math.log(2))/(f12*f21*w*math.pi)) # condutividade elétrica.
        print("A Condutividade elétrica é", sigma, "(Ωm)-¹")
if amostra == 2: # retangular
    if substrato == 1: # isolante
        sigma = float((G*math.log(2))/(f11*f22*w*math.pi)) # condutividade elétrica
        print("A Condutividade elétrica é", sigma, "(Ωm)-¹")
    if substrato == 2: # condutor
        sigma = float((G*math.log(2))/(f12*f22*w*math.pi)) # condutividade elétrica
        print("A Condutividade elétrica é", sigma, "(Ωm)-¹")