from socket import timeout
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic, QtCore

import sys

import numpy as np
from pexpect import TIMEOUT

import serial

import time

import serial.tools.list_ports

ser = 0

class PuertoSerie(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi('puerto/guiEspere.ui', self)

    def PROGR_TO_POSMEM(self, dispActual, progActual):
        """
        """

        # Version 1.
        #return ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )

        # Version 2.
        return ( 0x0040 * progActual )

    def DISP_TO_POSMEM_1(self, dispActual):
        """
        """

        # Version 1.
        #return ( 0x4020 * dispActual )

        # Version 2.
        if(dispActual == 1):
            return 0x0000
        elif(dispActual == 2):
            return 0x40F0
        elif(dispActual == 3):
            return 0x4150
        elif(dispActual == 4):
            return 0x41B0
        elif(dispActual == 5):
            return 0x4210
        elif(dispActual == 6):
            return 0x4270
        elif(dispActual == 7):
            return 0x42D0
        elif(dispActual == 8):
            return 0x4330
        else:
            return 0x0000

    def DISP_TO_POSMEM_CALIB(self, dispActual):
        """
        """

        base = 0x0050

        if(dispActual == 0):
            return 0x0000
        elif(dispActual == 1):
            return 0x40B0 - base
        elif(dispActual == 2):
            return 0x4110 - base
        elif(dispActual == 3):
            return 0x4170 - base
        elif(dispActual == 4):
            return 0x41D0 - base
        elif(dispActual == 5):
            return 0x4230 - base
        elif(dispActual == 6):
            return 0x4290 - base
        elif(dispActual == 7):
            return 0x42F0 - base
        else:
            return 0x0000

    def DISP_TO_POSMEM_SERV(self, dispActual):
        """
        """

        base = 0x0090

        if(dispActual == 0):
            return 0x0000
        elif(dispActual == 1):
            return 0x40F0 - base
        elif(dispActual == 2):
            return 0x4150 - base
        elif(dispActual == 3):
            return 0x41B0 - base
        elif(dispActual == 4):
            return 0x4210 - base
        elif(dispActual == 5):
            return 0x4270 - base
        elif(dispActual == 6):
            return 0x42D0 - base
        elif(dispActual == 7):
            return 0x4330 - base
        else:
            return 0x0000

    def conversorDuty(self, tension):
        """
        Tension -> Duty
        """

        x = np.array([10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,470,480,490,500,510,520,530,540,550,560,570,580,590,600,610,620,630,640,650,660,670,680,690,700,710,720,730,740,750,760,770,780,790,800,810,820,830,840,850,860,870,880,890,900,910,920,930,940,950,960,970,980,990])
        #y = np.array([0.228,0.42,0.602,0.778,0.973,1.143,1.314,1.477,1.662,1.821,1.964,2.146,2.299,2.424,2.581,2.715,2.882,3.01,3.152,3.286,3.433,3.567,3.701,3.833,3.97,4.1,4.23,4.36,4.5,4.63,4.76,4.86,4.98,5.08,5.22,5.31,5.42,5.53,5.64,5.74,5.85,5.95,6.07,6.16,6.26,6.4,6.51,6.6,6.71,6.8,6.9,7.02,7.1,7.18,7.25,7.31,7.39,7.49,7.58,7.68,7.77,7.89,7.96,8.06,8.09,8.15,8.22,8.31,8.39,8.5,8.57,8.69,8.76,8.84,8.91,9,9.07,9.11,9.17,9.25,9.29,9.38,9.45,9.51,9.58,9.65,9.7,9.79,9.87,9.91,9.98,10.06,10.12,10.19,10.25,10.34,10.37,10.44,10.49])
        y = np.array([0.262,0.517,0.745,0.958,1.184,1.382,1.572,1.754,1.955,2.13,2.305,2.483,2.673,2.841,3.009,3.17,3.351,3.507,3.662,3.82,3.985,4.13,4.27,4.41,4.58,4.71,4.85,4.99,5.12,5.27,5.41,5.53,5.67,5.81,5.93,6.06,6.19,6.32,6.44,6.56,6.67,6.8,6.91,7.02,7.14,7.26,7.36,7.48,7.58,7.69,7.8,7.9,8,8.09,8.2,8.29,8.39,8.48,8.57,8.68,8.77,8.86,8.96,9.06,9.14,9.23,9.32,9.41,9.49,9.57,9.66,9.74,9.82,9.9,9.98,10.06,10.13,10.19,10.29,10.37,10.45,10.52,10.59,10.67,10.75,10.82,10.88,10.95,11.02,11.09,11.15,11.23,11.29,11.36,11.41,11.45,11.46,11.47,11.47])

        if(tension > 0):
            valor_1 = 0
            valor_1 = np.interp(tension, y, x)

        else:
            valor_1 = 0

        return valor_1

    def conversorTension(self, fuerza, calibracion, dispActual):
        """
        Fuerza -> Tension -> Duty
        """

        x = calibracion[dispActual, 0, 5:9 + 1]
        y = calibracion[dispActual, 0, 10:14 + 1]

        if(fuerza > 0):
            valor_1 = 0
            valor_1 = np.interp(fuerza, y, x)

            valor_2 = self.conversorDuty(valor_1)

        else:
            valor_1 = 0
            valor_2 = 0

        valor_2 = int(round(valor_2))

        #print(x)
        #print(y)
        #print("Fuerza:", fuerza)
        #print("Tension:", valor_1)
        #print("% CS:", valor_2)

        return valor_2

    def conversorPorcentaje(self, intensidad, calibracion, dispActual):
        """
        Intensidad -> Porcentaje
        """

        x = calibracion[dispActual, 0, 15:19 + 1]
        y = calibracion[dispActual, 0, 20:24 + 1]        

        if(intensidad > 0):
            valor_1 = 0
            valor_1 = np.interp(intensidad, y, x)

            valor_2 = valor_1 * (7300 / 100)

        else:
            valor_1 = 0
            valor_2 = 0

        valor_2 = int(round(valor_2))
        return valor_2

    def conversorMiliVoltios(self, intensidad, calibracion, adc, dispActual):
        """
        Intensidad -> miliVoltios.
        """

        x = calibracion[dispActual, 0, 20:24 + 1]
        y = adc[dispActual, 0, :]

        x = [ x[0], x[-1] ]
        y = [ y[0], y[-1] ]        

        if(intensidad > 0):
            valor_1 = 0
            valor_1 = np.interp(intensidad, x, y)

        else:
            valor_1 = 0

        valor_1 = int(round(valor_1))

        print('- X:', x, '- Y:', y)
        print('- Intensidad: ', intensidad, '[KA]')
        print('- Valor_1: ', valor_1, '[mV]')
        print(' ')

        return valor_1

    def borrarEeprom(self):
        """
        """

        dato = 255
        size_EEPROM = 65535

        for i in range(0, size_EEPROM):
            self.barraProgreso( 100 * i / size_EEPROM )
            self.enviar(i, dato)

    def bloquearProgramas(self):
        """
        """

        STEP = 6
        self.barraProgreso( 0, STEP )

        D_INI_SOLD = 0x00B0

        MAX_DISP = 1
        MAX_PROG = 255        

        dato = 255
        cont = 0

        """ for i in range(0, MAX_DISP):

            dispActual = i
            for j in range(0, MAX_PROG+1):

                progActual = j                
                cont += 1
                
                #D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )
                D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

                self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.
                self.enviar(0x0032 + D_INI_SOLD + D_POSC_MEM, dato)                  # Dispositivo.

                self.barraProgreso( 100 * (j/MAX_PROG+1) ) """

        dispActual = 0
        for j in range(0, MAX_PROG+1):

            progActual = j                
            cont += 1

            D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

            self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.
            self.enviar(0x0032 + D_INI_SOLD + D_POSC_MEM, dato)                  # Dispositivo.

            self.barraProgreso( 100 * (j/MAX_PROG), STEP )

    def bloquearPrograma(self, dispositivo, programa):
        """
        Se usaba en tabla.py pero ahora no ... F
        """

        self.barraProgreso( 0 )

        D_INI_SOLD = 0x00B0

        dato = 255

        D_POSC_MEM = ( ( 0x4020 * (dispositivo - 0x0001) ) + ( 0x0040 * (programa - 0x0001) ) )
        self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.

        self.barraProgreso( 100 )

    def enviarDatosConfiguracion(self, cs):
        """
        """

        STEP = 1
        self.barraProgreso( 30, STEP )

        D_INI_CONF = 0x0000

        dato = cs['CONFIGURACION'][0][0][0] 
        self.enviar(0x0000 + D_INI_CONF, dato)          # Tipo de Soldadura.

        dato = cs['CONFIGURACION'][0][0][1]
        self.enviar(0x0001 + D_INI_CONF, dato)          # Aumento de Programa.

        dato = cs['CONFIGURACION'][0][0][2] / 10
        self.enviar(0x0002 + D_INI_CONF, dato)          # Fin de ciclo.

        dato = int(cs['CONFIGURACION'][0][0][3])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0003 + D_INI_CONF, dato_MSB)      # Conf. Varias.
        self.enviar(0x0004 + D_INI_CONF, dato_LSB)      # Conf. Varias.

        ################### Agregar Nombre, MAC, IP

        dato = cs['CONFIGURACION'][0][0][4]
        self.enviar(0x002F + D_INI_CONF, dato)          # Disp. Actual.

        dato = cs['CONFIGURACION'][0][0][5]
        self.enviar(0x0030 + D_INI_CONF, dato)          # Prog. Actual.

        dato = cs['CONFIGURACION'][0][0][6]
        self.enviar(0x0031 + D_INI_CONF, dato)          # Flags Inputs.

        self.barraProgreso( 100, STEP )

    def enviarDatosMonitor(self, cs, dispActual):
        """
        """

        STEP = 2
        self.barraProgreso( 30, STEP )

        D_INI_MONITOR = 0x0040

        #################### PARAMETROS USUARIOS.

        dato = cs['MONITOR'][0][0][0] 
        self.enviar(0x0000 + D_INI_MONITOR, dato)           # Tiempo 1.

        dato = cs['MONITOR'][0][0][1] 
        self.enviar(0x0001 + D_INI_MONITOR, dato)           # Tiempo 2.
        
        dato = int(cs['MONITOR'][0][0][5])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0002 + D_INI_MONITOR, dato_MSB)       # Fuerza.
        self.enviar(0x0003 + D_INI_MONITOR, dato_LSB)       # Fuerza.

        dato = int(cs['MONITOR'][0][0][3] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0004 + D_INI_MONITOR, dato_MSB)       # Intensidad.
        self.enviar(0x0005 + D_INI_MONITOR, dato_LSB)       # Intensidad.

        dato = cs['MONITOR'][0][0][2] 
        self.enviar(0x0006 + D_INI_MONITOR, dato)           # T. Sold.

        dato = cs['MONITOR'][0][0][4] 
        self.enviar(0x0007 + D_INI_MONITOR, dato)           # Tiempo 3.

        #################### PARAMETROS CONTROL (Conversion por regresion).

        # Fuerza -> conversor Tension -> conversor Duty -> dato_MSB y dato_LSB -> enviar
        # Intensidad -> conversor Porcentaje -> dato_MSB y dato_LSB -> enviar

        dato = self.conversorTension(cs['MONITOR'][0][0][5], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0008 + D_INI_MONITOR, dato_MSB)   # Fuerza.
        self.enviar(0x0009 + D_INI_MONITOR, dato_LSB)   # Fuerza.

        dato = self.conversorPorcentaje(cs['MONITOR'][0][0][3], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000A + D_INI_MONITOR, dato_MSB)   # Intensidad.
        self.enviar(0x000B + D_INI_MONITOR, dato_LSB)   # Intensidad.

        self.barraProgreso( 100, STEP ) 

    def enviarDatosCalibracion(self, cs, dispActual):
        """
        """

        STEP = 3

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        #################### PARAMETROS USUARIOS.        
        
        # Voltios Fuerza

        dato = int(cs['CALIBRACION'][dispActual][0][5] * 1000)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0000 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # Volt Fuerza 1.
        self.enviar(0x0001 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # Volt Fuerza 1.

        dato = int(cs['CALIBRACION'][dispActual][0][6] * 1000)    
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0002 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # Volt Fuerza 2.
        self.enviar(0x0003 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # Volt Fuerza 2.
        
        dato = int(cs['CALIBRACION'][dispActual][0][7] * 1000)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0004 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # Volt Fuerza 3.
        self.enviar(0x0005 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # Volt Fuerza 3.
        
        dato = int(cs['CALIBRACION'][dispActual][0][8] * 1000)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0006 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # Volt Fuerza 4.
        self.enviar(0x0007 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # Volt Fuerza 4.
        
        dato = int(cs['CALIBRACION'][dispActual][0][9] * 1000)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0008 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # Volt Fuerza 5.
        self.enviar(0x0009 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # Volt Fuerza 5.

        # Fuerza DaN

        dato = int(cs['CALIBRACION'][dispActual][0][10])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000A + D_INI_CALI + D_POSC_MEM, dato_MSB)          # DaN Fuerza 1.
        self.enviar(0x000B + D_INI_CALI + D_POSC_MEM, dato_LSB)          # DaN Fuerza 1.

        dato = int(cs['CALIBRACION'][dispActual][0][11])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000C + D_INI_CALI + D_POSC_MEM, dato_MSB)          # DaN Fuerza 2.
        self.enviar(0x000D + D_INI_CALI + D_POSC_MEM, dato_LSB)          # DaN Fuerza 2.

        dato = int(cs['CALIBRACION'][dispActual][0][12])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000E + D_INI_CALI + D_POSC_MEM, dato_MSB)          # DaN Fuerza 3.
        self.enviar(0x000F + D_INI_CALI + D_POSC_MEM, dato_LSB)          # DaN Fuerza 3.

        dato = int(cs['CALIBRACION'][dispActual][0][13])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0010 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # DaN Fuerza 4.
        self.enviar(0x0011 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # DaN Fuerza 4.

        dato = int(cs['CALIBRACION'][dispActual][0][14])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0012 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # DaN Fuerza 5.
        self.enviar(0x0013 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # DaN Fuerza 5.

        # Intensidad %

        dato = cs['CALIBRACION'][dispActual][0][15] 
        self.enviar(0x0014 + D_INI_CALI + D_POSC_MEM, dato)       # % Intensidad 1.

        dato = cs['CALIBRACION'][dispActual][0][16] 
        self.enviar(0x0015 + D_INI_CALI + D_POSC_MEM, dato)       # % Intensidad 2.

        dato = cs['CALIBRACION'][dispActual][0][17] 
        self.enviar(0x0016 + D_INI_CALI + D_POSC_MEM, dato)       # % Intensidad 3.

        dato = cs['CALIBRACION'][dispActual][0][18] 
        self.enviar(0x0017 + D_INI_CALI + D_POSC_MEM, dato)       # % Intensidad 4.

        dato = cs['CALIBRACION'][dispActual][0][19] 
        self.enviar(0x0018 + D_INI_CALI + D_POSC_MEM, dato)       # % Intensidad 5.

        # Intensidad KA

        dato = int(cs['CALIBRACION'][dispActual][0][20] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0019 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # KA Intensidad 1.
        self.enviar(0x001A + D_INI_CALI + D_POSC_MEM, dato_LSB)          # KA Intensidad 1.

        dato = int(cs['CALIBRACION'][dispActual][0][21] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001B + D_INI_CALI + D_POSC_MEM, dato_MSB)          # KA Intensidad 2.
        self.enviar(0x001C + D_INI_CALI + D_POSC_MEM, dato_LSB)          # KA Intensidad 2.

        dato = int(cs['CALIBRACION'][dispActual][0][22] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001D + D_INI_CALI + D_POSC_MEM, dato_MSB)          # KA Intensidad 3.
        self.enviar(0x001E + D_INI_CALI + D_POSC_MEM, dato_LSB)          # KA Intensidad 3.

        dato = int(cs['CALIBRACION'][dispActual][0][23] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001F + D_INI_CALI + D_POSC_MEM, dato_MSB)          # KA Intensidad 4.
        self.enviar(0x0020 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # KA Intensidad 4.

        dato = int(cs['CALIBRACION'][dispActual][0][24] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0021 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # KA Intensidad 5.
        self.enviar(0x0022 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # KA Intensidad 5. 

        #################### PARAMETROS CONTROL.

        dato = cs['CALIBRACION'][dispActual][0][0] 
        self.enviar(0x0027 + D_INI_CALI + D_POSC_MEM, dato)         # Tiempo Acerc.

        dato = cs['CALIBRACION'][dispActual][0][1] 
        self.enviar(0x0028 + D_INI_CALI + D_POSC_MEM, dato)         # Tiempo Apriete.  

        dato = int(cs['CALIBRACION'][dispActual][0][2])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0029 + D_INI_CALI + D_POSC_MEM, dato_MSB)     # Fuerza.
        self.enviar(0x002A + D_INI_CALI + D_POSC_MEM, dato_LSB)     # Fuerza.    

        dato = cs['CALIBRACION'][dispActual][0][3] 
        self.enviar(0x002B + D_INI_CALI + D_POSC_MEM, dato)         # Tiempo Sold.

        dato = cs['CALIBRACION'][dispActual][0][4] 
        self.enviar(0x002C + D_INI_CALI + D_POSC_MEM, dato)         # Tiempo Mant. 

        base = list(cs['DISP_LISTA'])
        base_max = len(base)
        self.barraProgreso( 100 * (dispActual/base_max), STEP )  

    def enviarDatosCalibracionADC(self, dispActual, numero_medicion, dato):
        """
        """

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        dato = int( round(dato) )
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        
        if(numero_medicion == 1):
            self.enviar(0x0035 + D_INI_CALI + D_POSC_MEM, dato_MSB) # ADC Medicion 1.
            self.enviar(0x0036 + D_INI_CALI + D_POSC_MEM, dato_LSB) # ADC Medicion 1. 

        elif(numero_medicion == 2):
            self.enviar(0x0037 + D_INI_CALI + D_POSC_MEM, dato_MSB) # ADC Medicion 2.
            self.enviar(0x0038 + D_INI_CALI + D_POSC_MEM, dato_LSB) # ADC Medicion 2. 

        elif(numero_medicion == 3):
            self.enviar(0x0039 + D_INI_CALI + D_POSC_MEM, dato_MSB) # ADC Medicion 3.
            self.enviar(0x003A + D_INI_CALI + D_POSC_MEM, dato_LSB) # ADC Medicion 3. 
            
        elif(numero_medicion == 4):
            self.enviar(0x003B + D_INI_CALI + D_POSC_MEM, dato_MSB) # ADC Medicion 4.
            self.enviar(0x003C + D_INI_CALI + D_POSC_MEM, dato_LSB) # ADC Medicion 4. 

        elif(numero_medicion == 5):
            self.enviar(0x003D + D_INI_CALI + D_POSC_MEM, dato_MSB) # ADC Medicion 5.
            self.enviar(0x003E + D_INI_CALI + D_POSC_MEM, dato_LSB) # ADC Medicion 5. 

        else:
            pass

    def enviarDatosServicios(self, cs, dispActual):
        """
        """

        STEP = 4

        D_INI_SERV = 0x0090
        D_POSC_MEM = self.DISP_TO_POSMEM_SERV(dispActual)

        #################### PARAMETROS USUARIOS.

        dato = int(cs['SERVICIOS'][dispActual][0][2])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0000 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Fuerza 1.
        self.enviar(0x0001 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Fuerza 1.

        dato = int(cs['SERVICIOS'][dispActual][0][3])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0002 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Fuerza 2.
        self.enviar(0x0003 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Fuerza 2.

        #################### PARAMETROS CONTROL.

        dato = int(cs['SERVICIOS'][dispActual][0][6])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0004 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Puntos.
        self.enviar(0x0005 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Puntos.

        dato = int(cs['SERVICIOS'][dispActual][0][7])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0006 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Alarma 1.
        self.enviar(0x0007 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Alarma 1.

        dato = int(cs['SERVICIOS'][dispActual][0][8])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0008 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Cont. 1.
        self.enviar(0x0009 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Cont. 1.

        dato = int(cs['SERVICIOS'][dispActual][0][9])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000A + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Fresado.
        self.enviar(0x000B + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Fresado.

        dato = int(cs['SERVICIOS'][dispActual][0][10])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000C + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Alarma 2.
        self.enviar(0x000D + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Alarma 2.

        dato = int(cs['SERVICIOS'][dispActual][0][11])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000E + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Cont. 2.
        self.enviar(0x000F + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Cont. 2.

        #dato = int(cs['SERVICIOS'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0010 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Punto Pieza.
        #self.enviar(0x0011 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Punto Pieza.

        #dato = int(cs['SERVICIOS'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0012 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Cont. 3.
        #self.enviar(0x0013 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Cont. 3.

        dato = self.conversorTension(cs['SERVICIOS'][dispActual][0][2], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0014 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Fuerza 1.
        self.enviar(0x0015 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Fuerza 1.

        dato = self.conversorTension(cs['SERVICIOS'][dispActual][0][3], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0016 + D_INI_SERV + D_POSC_MEM, dato_MSB)          # Fuerza 2.
        self.enviar(0x0017 + D_INI_SERV + D_POSC_MEM, dato_LSB)          # Fuerza 2.

        dato = int(cs['SERVICIOS'][dispActual][0][0])
        self.enviar(0x0018 + D_INI_SERV + D_POSC_MEM, dato)          # Tiempo 1.

        dato = int(cs['SERVICIOS'][dispActual][0][1])
        self.enviar(0x0019 + D_INI_SERV + D_POSC_MEM, dato)          # Tiempo 2.

        dato = int(cs['SERVICIOS'][dispActual][0][4])
        self.enviar(0x001A + D_INI_SERV + D_POSC_MEM, dato)          # Curva.

        dato = int(cs['SERVICIOS'][dispActual][0][5])
        self.enviar(0x001B + D_INI_SERV + D_POSC_MEM, dato)          # % Incremento.

        base = list(cs['DISP_LISTA'])
        base_max = len(base)
        self.barraProgreso( 100 * (dispActual/base_max), STEP ) 

    def enviarDatosSoldadura(self, cs, dispActual, progActual):
        """
        """

        #self.barraProgreso(100 / 5 * 5)

        print("- DISP:", dispActual + 1, "- PROG:", progActual + 1)

        D_INI_SOLD = 0x00B0
        #D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

        #################### PARAMETROS USUARIOS.

        # 1

        dispActual = 0
    
        dato = int(cs['SOLDADURA'][dispActual][progActual][0])
        self.enviar(0x0000 + D_INI_SOLD + D_POSC_MEM, dato)                  # Acercamiento.
        
        dato = int(cs['SOLDADURA'][dispActual][progActual][1])
        self.enviar(0x0001 + D_INI_SOLD + D_POSC_MEM, dato)                  # Apriete.

        dato = int(cs['SOLDADURA'][dispActual][progActual][2])
        self.enviar(0x0002 + D_INI_SOLD + D_POSC_MEM, dato)                  # Repeticion.

        # 2

        dato = int(cs['SOLDADURA'][dispActual][progActual][3])
        self.enviar(0x0003 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Sold. 1.

        dato = int(cs['SOLDADURA'][dispActual][progActual][4] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0004 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 1.
        self.enviar(0x0005 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 1.

        dato = int(cs['SOLDADURA'][dispActual][progActual][5])
        self.enviar(0x0006 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Frio 1.

        # 3

        dato = int(cs['SOLDADURA'][dispActual][progActual][6])
        self.enviar(0x0007 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Sold. 2.

        dato = int(cs['SOLDADURA'][dispActual][progActual][7] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0008 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 2.
        self.enviar(0x0009 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 2.

        dato = int(cs['SOLDADURA'][dispActual][progActual][8])
        self.enviar(0x000A + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Frio 2.

        dato = int(cs['SOLDADURA'][dispActual][progActual][9])
        self.enviar(0x000B + D_INI_SOLD + D_POSC_MEM, dato)                  # Impulsos.

        # 4 

        dato = int(cs['SOLDADURA'][dispActual][progActual][10])
        self.enviar(0x000C + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Sold. 3.

        dato = int(cs['SOLDADURA'][dispActual][progActual][11] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x000D + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 3.
        self.enviar(0x000E + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 3.

        dato = int(cs['SOLDADURA'][dispActual][progActual][12])
        self.enviar(0x000F + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Frio 3.

        # 5

        dato = int(cs['SOLDADURA'][dispActual][progActual][13])
        self.enviar(0x0010 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Sold. 4.

        dato = int(cs['SOLDADURA'][dispActual][progActual][14] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0011 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 4.
        self.enviar(0x0012 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 4.

        # 6

        dato = int(cs['SOLDADURA'][dispActual][progActual][15])
        self.enviar(0x0013 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Sold. 5.

        dato = int(cs['SOLDADURA'][dispActual][progActual][16] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0014 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 5.
        self.enviar(0x0015 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 5.

        # 7

        dato = int(cs['SOLDADURA'][dispActual][progActual][17])
        self.enviar(0x0016 + D_INI_SOLD + D_POSC_MEM, dato)                  # T. Forja.

        dato = int(cs['SOLDADURA'][dispActual][progActual][18])
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0017 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Fuerza.
        self.enviar(0x0018 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Fuerza.

        # 8 

        dato = int(cs['SOLDADURA'][dispActual][progActual][19])
        self.enviar(0x0019 + D_INI_SOLD + D_POSC_MEM, dato)                  # Tolerancia 1.

        dato = int(cs['SOLDADURA'][dispActual][progActual][20])
        self.enviar(0x001A + D_INI_SOLD + D_POSC_MEM, dato)                  # Tolerancia 2.

        #################### PARAMETROS CONTROL.

        #dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][4], cs['CALIBRACION'], dispActual)
        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][4] + cs['SOLDADURA'][dispActual][progActual][22], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001B + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 1.
        self.enviar(0x001C + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 1.

        #dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][7], cs['CALIBRACION'], dispActual)
        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][7] + cs['SOLDADURA'][dispActual][progActual][22], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001D + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 2.
        self.enviar(0x001E + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 2.

        #dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][11], cs['CALIBRACION'], dispActual)
        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][11] + cs['SOLDADURA'][dispActual][progActual][22], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001F + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 3.
        self.enviar(0x0020 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 3.

        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][14], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0021 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 4.
        self.enviar(0x0022 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 4.

        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][16], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0023 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 5.
        self.enviar(0x0024 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 5.

        #dato = self.conversorTension(cs['SOLDADURA'][dispActual][progActual][18], cs['CALIBRACION'], dispActual)
        dato = self.conversorTension(cs['SOLDADURA'][dispActual][progActual][18] + cs['SOLDADURA'][dispActual][progActual][23], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0025 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Fuerza.
        self.enviar(0x0026 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Fuerza.

        dato = int(cs['SOLDADURA'][dispActual][progActual][21])
        self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.

        #################### PARAMETROS AUXILIARES.

        dato = int(cs['SOLDADURA'][dispActual][progActual][22] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0028 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Offset Intensidad usuario.
        self.enviar(0x0029 + D_INI_SOLD + D_POSC_MEM, dato_LSB)     

        dato = int(cs['SOLDADURA'][dispActual][progActual][23] * 100)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x002A + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Offset Fuerza usuario.
        self.enviar(0x002B + D_INI_SOLD + D_POSC_MEM, dato_LSB)     
    
    def enviarDatosSoldaduraADC(self, cs, adc, dispActual, progActual):
        """
        """

        D_INI_SOLD = 0x00B0
        #D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)
        
        print('-'*50, 'Intensidad Soldadura.')
        dato = self.conversorMiliVoltios( cs['SOLDADURA'][dispActual][progActual][7], cs['CALIBRACION'], adc['CALIBRACION_I'], dispActual )
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0030 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 2 en mV.
        self.enviar(0x0031 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 2 en mV.

        # faltan agregar los limites superior e inferior.        
        
        print('-'*50, 'Tolerancia Superior.')
        dato_MAX_percent = cs['SOLDADURA'][dispActual][progActual][7] * ( 1 + ( cs['SOLDADURA'][dispActual][progActual][20] / 100 ) )
        dato = self.conversorMiliVoltios( dato_MAX_percent, cs['CALIBRACION'], adc['CALIBRACION_I'], dispActual )
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x002C + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Tolerancia superior en mV.
        self.enviar(0x002D + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Tolerancia superior en mV.
        
        print('-'*50, 'Tolerancia Inferior.')
        dato_MIN_percent = cs['SOLDADURA'][dispActual][progActual][7] * ( 1 - ( cs['SOLDADURA'][dispActual][progActual][19] / 100 ) )
        dato = self.conversorMiliVoltios( dato_MIN_percent, cs['CALIBRACION'], adc['CALIBRACION_I'], dispActual )
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x002E + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Tolerancia inferior en mV.
        self.enviar(0x002F + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Tolerancia inferior en mV.     

    def enviarDatosSoldaduraDispositivo(self, dispActual, progActual):
        """
        """

        D_INI_SOLD = 0x00B0
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

        dato = int(dispActual + 1)
        self.enviar(0x0032 + D_INI_SOLD + D_POSC_MEM, dato)

    def recibirDatosConfiguracion(self, cs):
        """
        """

        STEP = 1
        self.barraProgreso( 20, STEP )

        D_INI_CONF = 0x0000

        dato = self.recibir(0x0000 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][0] = dato             # Tipo de Soldadura.

        dato = self.recibir(0x0001 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][1] = dato             # Aumento de Programa.
        
        dato = self.recibir(0x0002 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][2] = dato * 10        # Fin de ciclo.

        dato_MSB = self.recibir(0x0003 + D_INI_CONF)
        dato_LSB = self.recibir(0x0004 + D_INI_CONF)
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CONFIGURACION'][0][0][3] =  dato            # Conf. Varias.

        ################### Agregar Nombre, MAC, IP

        dato = self.recibir(0x002F + D_INI_CONF)
        cs['CONFIGURACION'][0][0][4] = dato             # Disp. Actual.

        dato = self.recibir(0x0030 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][5] = dato             # Prog. Actual.

        dato = self.recibir(0x0031 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][6] = dato             # Flags Inputs.

        self.barraProgreso( 100, STEP )

        return cs['CONFIGURACION']

    def recibirDatosMonitor(self, cs, dispActual):
        """
        """

        STEP = 2
        self.barraProgreso( 20, STEP )

        D_INI_MONITOR = 0x0040

        cs['MONITOR'][0][0][0] = self.recibir(0x0000 + D_INI_MONITOR)   # Tiempo 1.

        cs['MONITOR'][0][0][1] = self.recibir(0x0001 + D_INI_MONITOR)   # Tiempo 2.
        
        
        dato_MSB = self.recibir(0x0002 + D_INI_MONITOR)   
        dato_LSB = self.recibir(0x0003 + D_INI_MONITOR)  
        dato = (dato_MSB << 8) + dato_LSB
        cs['MONITOR'][0][0][5] =  dato                                  # Fuerza.

        
        dato_MSB = self.recibir(0x0004 + D_INI_MONITOR)                 
        dato_LSB = self.recibir(0x0005 + D_INI_MONITOR)                 
        dato = (dato_MSB << 8) + dato_LSB
        cs['MONITOR'][0][0][3] = dato / 100                             # Intensidad.

        dato = self.recibir(0x0006 + D_INI_MONITOR)                     # T. Sold.
        cs['MONITOR'][0][0][2] = dato        

        dato = self.recibir(0x0007 + D_INI_MONITOR)                     # Tiempo 3.
        cs['MONITOR'][0][0][4] = dato

        self.barraProgreso( 100, STEP )       

        return cs['MONITOR']

    def recibirDatosCalibracion(self, cs, dispActual):
        """
        """

        STEP = 4

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        #################### PARAMETROS USUARIOS.        
        
        # Voltios Fuerza
        
        dato_MSB = self.recibir(0x0000 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0001 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][5] = dato / 1000           # Volt Fuerza 1.

        dato_MSB = self.recibir(0x0002 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0003 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][6] = dato / 1000           # Volt Fuerza 2.

        dato_MSB = self.recibir(0x0004 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0005 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][7] = dato / 1000           # Volt Fuerza 3.

        dato_MSB = self.recibir(0x0006 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0007 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][8] = dato / 1000           # Volt Fuerza 4.

        dato_MSB = self.recibir(0x0008 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0009 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][9] = dato / 1000           # Volt Fuerza 5.

        # Fuerza DaN
        
        dato_MSB = self.recibir(0x000A + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x000B + D_INI_CALI + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB  
        cs['CALIBRACION'][dispActual][0][10] = dato                 # DaN Fuerza 1.

        dato_MSB = self.recibir(0x000C + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x000D + D_INI_CALI + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB  
        cs['CALIBRACION'][dispActual][0][11] = dato                 # DaN Fuerza 2.

        dato_MSB = self.recibir(0x000E + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x000F + D_INI_CALI + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB  
        cs['CALIBRACION'][dispActual][0][12] = dato                 # DaN Fuerza 3.

        dato_MSB = self.recibir(0x0010 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0011 + D_INI_CALI + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB  
        cs['CALIBRACION'][dispActual][0][13] = dato                 # DaN Fuerza 4.

        dato_MSB = self.recibir(0x0012 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0013 + D_INI_CALI + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB  
        cs['CALIBRACION'][dispActual][0][14] = dato                 # DaN Fuerza 5.

        # Intensidad %

        dato = self.recibir(0x0014 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][15] = dato                 # % Intensidad 1.

        dato = self.recibir(0x0015 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][16] = dato                 # % Intensidad 2.

        dato = self.recibir(0x0016 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][17] = dato                 # % Intensidad 3.

        dato = self.recibir(0x0017 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][18] = dato                 # % Intensidad 4.

        dato = self.recibir(0x0018 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][19] = dato                 # % Intensidad 5.

        # Intensidad KA
        
        dato_MSB = self.recibir(0x0019 + D_INI_CALI + D_POSC_MEM) 
        dato_LSB = self.recibir(0x001A + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][20] = dato / 100           # KA Intensidad 1.

        dato_MSB = self.recibir(0x001B + D_INI_CALI + D_POSC_MEM) 
        dato_LSB = self.recibir(0x001C + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][21] = dato / 100           # KA Intensidad 2.

        dato_MSB = self.recibir(0x001D + D_INI_CALI + D_POSC_MEM) 
        dato_LSB = self.recibir(0x001E + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][22] = dato / 100           # KA Intensidad 3.

        dato_MSB = self.recibir(0x001F + D_INI_CALI + D_POSC_MEM) 
        dato_LSB = self.recibir(0x0020 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][23] = dato / 100           # KA Intensidad 4.

        dato_MSB = self.recibir(0x0021 + D_INI_CALI + D_POSC_MEM) 
        dato_LSB = self.recibir(0x0022 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][24] = dato / 100           # KA Intensidad 5.   

        #################### PARAMETROS CONTROL.

        dato = self.recibir(0x0027 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][0] = dato                  # Tiempo Acerc.  

        dato = self.recibir(0x0028 + D_INI_CALI + D_POSC_MEM)  
        cs['CALIBRACION'][dispActual][0][1] = dato                  # Tiempo Apriete.

        dato_MSB = self.recibir(0x0029 + D_INI_CALI + D_POSC_MEM)  
        dato_LSB = self.recibir(0x002A + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        cs['CALIBRACION'][dispActual][0][2] = dato                  # Fuerza.                     

        dato = self.recibir(0x002B + D_INI_CALI + D_POSC_MEM)
        cs['CALIBRACION'][dispActual][0][3] = dato                  # Tiempo Sold.

        dato = self.recibir(0x002C + D_INI_CALI + D_POSC_MEM)
        cs['CALIBRACION'][dispActual][0][4] = dato                  # Tiempo Mant.   

        base = list(cs['DISP_LISTA'])
        base_max = len(base)
        self.barraProgreso( 100 * (dispActual/base_max), STEP )

        return cs['CALIBRACION']

    def recibirDatosCalibracionADC(self, adc, dispActual):
        """
        """

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        dato_MSB = self.recibir(0x0035 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0036 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        adc['CALIBRACION_I'][dispActual][0][0] = dato               # adc 1.

        dato_MSB = self.recibir(0x0037 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x0038 + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        adc['CALIBRACION_I'][dispActual][0][1] = dato               # adc 2.

        dato_MSB = self.recibir(0x0039 + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x003A + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        adc['CALIBRACION_I'][dispActual][0][2] = dato               # adc 3.

        dato_MSB = self.recibir(0x003B + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x003C + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        adc['CALIBRACION_I'][dispActual][0][3] = dato               # adc 4.

        dato_MSB = self.recibir(0x003D + D_INI_CALI + D_POSC_MEM)
        dato_LSB = self.recibir(0x003E + D_INI_CALI + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB 
        adc['CALIBRACION_I'][dispActual][0][4] = dato               # adc 5.

        return adc['CALIBRACION_I']

    def recibirDatosServicios(self, cs, dispActual):
        """
        """

        STEP = 5

        D_INI_SERV = 0x0090
        D_POSC_MEM = self.DISP_TO_POSMEM_SERV(dispActual)
        
        dato_MSB = self.recibir(0x0000 + D_INI_SERV + D_POSC_MEM)          
        dato_LSB = self.recibir(0x0001 + D_INI_SERV + D_POSC_MEM)          
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][2] = dato                    # Fuerza 1.
        
        dato_MSB = self.recibir(0x0002 + D_INI_SERV + D_POSC_MEM)          
        dato_LSB = self.recibir(0x0003 + D_INI_SERV + D_POSC_MEM)          
        dato = (dato_MSB << 8) + dato_LSB 
        cs['SERVICIOS'][dispActual][0][3] = dato                    # Fuerza 2.
        
        dato_MSB = self.recibir(0x0004 + D_INI_SERV + D_POSC_MEM)
        dato_LSB = self.recibir(0x0005 + D_INI_SERV + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][6] = dato                    # Puntos.
        
        dato_MSB = self.recibir(0x0006 + D_INI_SERV + D_POSC_MEM)           
        dato_LSB = self.recibir(0x0007 + D_INI_SERV + D_POSC_MEM)           
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][7] = dato                    # Alarma 1.
        
        dato_MSB = self.recibir(0x0008 + D_INI_SERV + D_POSC_MEM)         
        dato_LSB = self.recibir(0x0009 + D_INI_SERV + D_POSC_MEM)         
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][8] = dato                    # Cont. 1.
        
        dato_MSB = self.recibir(0x000A + D_INI_SERV + D_POSC_MEM)           
        dato_LSB = self.recibir(0x000B + D_INI_SERV + D_POSC_MEM)           
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][9] = dato                    # Fresado.
        
        dato_MSB = self.recibir(0x000C + D_INI_SERV + D_POSC_MEM)    
        dato_LSB = self.recibir(0x000D + D_INI_SERV + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB
        cs['SERVICIOS'][dispActual][0][10] = dato                   # Alarma 2.
        
        dato_MSB = self.recibir(0x000E + D_INI_SERV + D_POSC_MEM)         
        dato_LSB = self.recibir(0x000F + D_INI_SERV + D_POSC_MEM)          
        dato = (dato_MSB << 8) + dato_LSB 
        cs['SERVICIOS'][dispActual][0][11] = dato                   # Cont. 2.

        #dato_MSB = self.recibir(0x0010 + D_INI_SERV + D_POSC_MEM)          
        #dato_LSB = self.recibir(0x0011 + D_INI_SERV + D_POSC_MEM)        
        #dato = (dato_MSB << 8) + dato_LSB
        # cs['SERVICIOS'][dispActual][0][0] = dato                  # Punto Pieza.
        
        #dato_MSB = self.recibir(0x0012 + D_INI_SERV + D_POSC_MEM)          
        #dato_LSB = self.recibir(0x0013 + D_INI_SERV + D_POSC_MEM)          
        #dato = (dato_MSB << 8) + dato_LSB 
        # cs['SERVICIOS'][dispActual][0][0] = dato                  # Cont. 3.        
           
        dato = self.recibir(0x0018 + D_INI_SERV + D_POSC_MEM)   
        cs['SERVICIOS'][dispActual][0][0] = dato                    # Tiempo 1.         
             
        dato = self.recibir(0x0019 + D_INI_SERV + D_POSC_MEM)  
        cs['SERVICIOS'][dispActual][0][1] = dato                    # Tiempo 2.          
             
        dato = self.recibir(0x001A + D_INI_SERV + D_POSC_MEM)  
        cs['SERVICIOS'][dispActual][0][4] = dato                    # Curva.          
            
        dato = self.recibir(0x001B + D_INI_SERV + D_POSC_MEM)  
        cs['SERVICIOS'][dispActual][0][5] = dato                    # % Incremento.   

        base = list(cs['DISP_LISTA'])
        base_max = len(base)
        self.barraProgreso( 100 * (dispActual/base_max), STEP )  

        return cs['SERVICIOS']

    def recibirDatosSoldadura(self, cs, dispActual, progActual):
        """
        """

        #self.barraProgreso(100 / 5 * 5)
        #self.barraProgreso( 100 * (progActual/255) )

        #print("- DISP:", dispActual + 1, "- PROG:", progActual + 1)
        print("- DISP:", dispActual, "- PROG:", progActual + 1)

        D_INI_SOLD = 0x00B0
        #D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

        dispActual = 0 

        # 1

        dato = self.recibir(0x0000 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][0] = dato           # Acercamiento.
        
        dato = self.recibir(0x0001 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][1] = dato           # Apriete.   

        dato = self.recibir(0x0002 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][2] = dato           # Repeticion.
        
        # 2

        dato = self.recibir(0x0003 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][3] = dato           # T. Sold. 1.
        
        dato_MSB = self.recibir(0x0004 + D_INI_SOLD + D_POSC_MEM)  
        dato_LSB = self.recibir(0x0005 + D_INI_SOLD + D_POSC_MEM)  
        dato = (dato_MSB << 8) + dato_LSB 
        cs['SOLDADURA'][dispActual][progActual][4] = dato / 100     # Intensidad 1.     

        dato = self.recibir(0x0006 + D_INI_SOLD + D_POSC_MEM)                 
        cs['SOLDADURA'][dispActual][progActual][5] = dato           # T. Frio 1.

        # 3

        dato = self.recibir(0x0007 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][6] = dato           # T. Sold. 2.
        
        dato_MSB = self.recibir(0x0008 + D_INI_SOLD + D_POSC_MEM)  
        dato_LSB = self.recibir(0x0009 + D_INI_SOLD + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB
        cs['SOLDADURA'][dispActual][progActual][7] = dato / 100     # Intensidad 2.

        dato = self.recibir(0x000A + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][8] = dato           # T. Frio 2.

        dato = self.recibir(0x000B + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][9] = dato           # Impulsos.

        # 4 

        dato = self.recibir(0x000C + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][10] = dato          # T. Sold. 3.
        
        dato_MSB = self.recibir(0x000D + D_INI_SOLD + D_POSC_MEM)      
        dato_LSB = self.recibir(0x000E + D_INI_SOLD + D_POSC_MEM)    
        dato = (dato_MSB << 8) + dato_LSB 
        cs['SOLDADURA'][dispActual][progActual][11] = dato / 100    # Intensidad 3.

        dato = self.recibir(0x000F + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][12] = dato          # T. Frio 3.      

        # 5

        dato = self.recibir(0x0010 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][13] = dato          # T. Sold. 4.
        
        dato_MSB = self.recibir(0x0011 + D_INI_SOLD + D_POSC_MEM) 
        dato_LSB = self.recibir(0x0012 + D_INI_SOLD + D_POSC_MEM)
        dato = (dato_MSB << 8) + dato_LSB
        cs['SOLDADURA'][dispActual][progActual][14] = dato / 100    # Intensidad 4.

        # 6

        dato = self.recibir(0x0013 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][15] = dato          # T. Sold. 5.
        
        dato_MSB = self.recibir(0x0014 + D_INI_SOLD + D_POSC_MEM)  
        dato_LSB = self.recibir(0x0015 + D_INI_SOLD + D_POSC_MEM) 
        dato = (dato_MSB << 8) + dato_LSB
        cs['SOLDADURA'][dispActual][progActual][16] = dato / 100    # Intensidad 5.

        # 7

        dato = self.recibir(0x0016 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][17] = dato          # T. Forja.
        
        dato_MSB = self.recibir(0x0017 + D_INI_SOLD + D_POSC_MEM)     
        dato_LSB = self.recibir(0x0018 + D_INI_SOLD + D_POSC_MEM)     
        dato = (dato_MSB << 8) + dato_LSB
        cs['SOLDADURA'][dispActual][progActual][18] = dato          # Fuerza.

        # 8 

        dato = self.recibir(0x0019 + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][19] = dato          # Tolerancia 1.    

        dato = self.recibir(0x001A + D_INI_SOLD + D_POSC_MEM)                  
        cs['SOLDADURA'][dispActual][progActual][20] = dato          # Tolerancia 2.     

        dato = self.recibir(0x0027 + D_INI_SOLD + D_POSC_MEM)
        cs['SOLDADURA'][dispActual][progActual][21] = dato          # Comportamiento.      

        # Parametros Auxiliares.

        dato_MSB = self.recibir(0x0028 + D_INI_SOLD + D_POSC_MEM)     
        dato_LSB = self.recibir(0x0029 + D_INI_SOLD + D_POSC_MEM)     
        dato = (dato_MSB << 8) + dato_LSB                
        cs['SOLDADURA'][dispActual][progActual][22] = dato / 100    # Offset Intensidad.    

        dato_MSB = self.recibir(0x002A + D_INI_SOLD + D_POSC_MEM)     
        dato_LSB = self.recibir(0x002B + D_INI_SOLD + D_POSC_MEM)     
        dato = (dato_MSB << 8) + dato_LSB                
        cs['SOLDADURA'][dispActual][progActual][23] = dato / 100    # Offset Fuerza.                      

        return cs['SOLDADURA']

    def recibirDatosSoldaduraADC(self, adc, dispActual, progActual):
        """
        """

        D_INI_SOLD = 0x00B0
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

        dato_MSB = self.recibir(0x002A + D_INI_SOLD + D_POSC_MEM)     
        dato_LSB = self.recibir(0x002B + D_INI_SOLD + D_POSC_MEM)     
        dato = (dato_MSB << 8) + dato_LSB                
        adc['SOLDADURA_I'][dispActual][progActual][0] = dato          # Soldadura 2 en mV.  

        return adc['SOLDADURA_I']

    def recibirDatosSoldaduraDispositivo(self, dispActual, progActual):
        """
        """

        STEP = 3

        D_INI_SOLD = 0x00B0
        D_POSC_MEM = self.PROGR_TO_POSMEM(dispActual, progActual)

        data_1 = 0
        data_2 = 0
        data_1 = self.recibir(0x0027 + D_INI_SOLD + D_POSC_MEM) # Comportamiento
        data_2 = self.recibir(0x0032 + D_INI_SOLD + D_POSC_MEM) # Dispositivo
        
        self.barraProgreso( 100 * (progActual/256), STEP )

        if( ( data_1 != 0 and data_1 != 255 ) and ( data_2 < 9 ) ):
            #print('- Comportamiento: ', data_1, ' - Dispositivo: ', data_2)
            pass
        else:
            data_1 = 0
            data_2 = 0

        return data_1, data_2

    def recibirDatosHistoricos(self, cant):
        """  
        MAX_HIST: es la cantidad maxima de historicos que se pueden acumular.
        """

        self.barraProgreso(0, 1)

        MAX_HIST = 200

        D_INI_HISTORIAL = 0x4350
        D_INI_CONF = 0x0000
        CAMBIO = 0

        dato_MSB = self.recibir(0x003A + D_INI_CONF)  
        dato_LSB = self.recibir(0x003B + D_INI_CONF)  
        contador = (dato_MSB << 8) + dato_LSB
        if(contador > MAX_HIST or contador < 1): contador = 1

        # Generador del vector programas.
        vect_prog = []
        posicion_inicial = 0
        aux_1 = contador - cant

        if(aux_1 > 0):
            posicion_inicial = aux_1 + 1            
            for i in range(posicion_inicial, contador+1): vect_prog.append(i)
            
        else:
            posicion_inicial = MAX_HIST - abs(aux_1) + 1            
            for i in range(posicion_inicial, MAX_HIST+1): vect_prog.append(i)                
            for i in range(1, contador+1): vect_prog.append(i)

        # Envio de informacion.
        cont = 0
        len_array = len(vect_prog)
        array = np.zeros((MAX_HIST+1, 7))
        for i in vect_prog:
            CAMBIO = (i-1) * 0x0020
            disp_actual = self.recibir(0x0000 + D_INI_HISTORIAL + CAMBIO)                  
            prog_actual = self.recibir(0x0001 + D_INI_HISTORIAL + CAMBIO)

            dato_MSB = self.recibir(0x0002 + D_INI_HISTORIAL + CAMBIO)  
            dato_LSB = self.recibir(0x0003 + D_INI_HISTORIAL + CAMBIO)  
            i_programada = (dato_MSB << 8) + dato_LSB 

            dato_MSB = self.recibir(0x0004 + D_INI_HISTORIAL + CAMBIO)  
            dato_LSB = self.recibir(0x0005 + D_INI_HISTORIAL + CAMBIO)  
            i_medida = (dato_MSB << 8) + dato_LSB 

            ciclo_programado = self.recibir(0x0006 + D_INI_HISTORIAL + CAMBIO)  
            ciclo_medido = self.recibir(0x0007 + D_INI_HISTORIAL + CAMBIO)

            error = self.recibir(0x001F + D_INI_HISTORIAL + CAMBIO)

            array[i][0] = disp_actual
            array[i][1] = prog_actual
            array[i][2] = i_programada / 100
            array[i][3] = i_medida / 100
            array[i][4] = ciclo_programado
            array[i][5] = ciclo_medido
            array[i][6] = error

            cont += 1
            self.barraProgreso( round( (cont/len_array) * 100 ), 1 )

        #print(contador)
        #print(vect_prog)
        
        return array

    def medirFuerza(self, cs, dispActual, dato):
        """
        """

        STEP = 1
        self.barraProgreso( 10, STEP )

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        print("-Fuerza-")
        
        dato = int(self.conversorDuty(dato))
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0031 + D_INI_CALI + D_POSC_MEM, dato_MSB) # aux fuerza.
        self.enviar(0x0032 + D_INI_CALI + D_POSC_MEM, dato_LSB) # aux fuerza. 

        dato = "E"                                              # CS hay que calibrar. 
        ser.write( bytes(dato.encode()) )                       # Envio bandera calibracion.

        self.barraProgreso( 100, STEP )

    def medirIntensidad(self, cs, dispActual, dato):
        """
        """

        STEP = 2
        self.barraProgreso( 10, STEP )

        D_INI_CALI = 0x0050
        D_POSC_MEM = self.DISP_TO_POSMEM_CALIB(dispActual)

        # Fuerza.

        print("-Fuerza-")

        aux = self.conversorTension(cs['CALIBRACION'][dispActual][0][2], cs['CALIBRACION'], dispActual)
        aux_MSB = aux >> 8
        aux_LSB = aux & 0xFF
        self.enviar(0x0031 + D_INI_CALI + D_POSC_MEM, aux_MSB)  # aux fuerza.
        self.enviar(0x0032 + D_INI_CALI + D_POSC_MEM, aux_LSB)  # aux fuerza.  

        # Intensidad.

        print("-Intensidad-")

        dato = dato * 7300 / 100
        dato = int(round(dato))

        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0033 + D_INI_CALI + D_POSC_MEM, dato_MSB) # aux intensidad.
        self.enviar(0x0034 + D_INI_CALI + D_POSC_MEM, dato_LSB) # aux intensidad.      

        dato = "F"                                              # CS hay que calibrar. 
        ser.write( bytes(dato.encode()) )                       # Envio bandera calibracion.

        STEP = 1
        self.barraProgreso( 100, STEP )

    def monitorFuerza(self):
        """
        """

        # Fuerza.
        
        STEP = 3
        self.barraProgreso( 10, STEP )        

        print("-Fuerza-")

        dato = "G"                                              # CS vamos a monitor fuerza. 
        ser.write( bytes(dato.encode()) )                       # Envio bandera calibracion.

        self.barraProgreso( 100, STEP )

    def monitorIntensidad(self):
        """
        """

        # Intensidad.

        STEP = 4
        self.barraProgreso( 10, STEP )

        print("-Intensidad-")

        dato = "H"                                              # CS vamos a monito intensidad. 
        ser.write( bytes(dato.encode()) )                       # Envio bandera calibracion.
        
        self.barraProgreso( 100, STEP )

    def monitorEntradas(self):
        """  
        """

        TIEMPO_DATO = 0.035

        dato = "I"
        ser.write( bytes(dato.encode()) )
        time.sleep(TIEMPO_DATO)                     # Tiempo del CS.
        
        bytesToRead = ser.inWaiting()
        dato = ser.read(bytesToRead)
        dato = int(dato)

        #dato = 0b0000000000000000001
        
        return dato

    def confPuerto(self, puerto, estado):
        """
        estado = "OPEN"
        estado = "CLOSE"
        """

        global ser

        TIEMPO_CONEXION = 0.035                                                 # Tiempo para habilitar la conexion.
        VELOCIDAD = 9600                                                        # Velocidad del puerto.
        TIMEOUT = 0.035

        if(estado == "OPEN"):
            ser = serial.Serial(puerto, baudrate=VELOCIDAD, timeout=TIMEOUT)    # Configuro el puerto.
            time.sleep(TIEMPO_CONEXION)                                         # Retardo para establecer 
                                                                                # la conexión serial.
            
            ser.flushInput()                                                    # Limpio la entrada.
            ser.flushOutput()                                                   # Limpio la salida.

        else:

            dato = 0
            dato = 'Z'
            ser.write( bytes(dato.encode()) )
            
            ser.close()                                        # Cierro el puerto.

    def enviar(self, direccion, dato):
        """
        """

        global ser

        flagMBS  = "+"
        flagLBS  = "-"
        flagDATO = "_"

        QtCore.QCoreApplication.processEvents()

        TIEMPO_DATO = 0.035                         # Tiempo que le toma al CS 
                                                    # para guardar la informacion.  

        direccion_MSB = str(direccion >> 8)
        direccion_LSB = str(direccion & 0xFF)
        dato = str(int(dato))

        ser.write( bytes(direccion_MSB.encode()) )
        ser.write( bytes(flagMBS.encode()) )        # Direccion MSB.

        ser.write( bytes(direccion_LSB.encode()) )
        ser.write( bytes(flagLBS.encode()) )        # Direccion LSB.

        ser.write( bytes(dato.encode()) )
        ser.write( bytes(flagDATO.encode()) )       # Dato.

        time.sleep(TIEMPO_DATO)                     # Tiempo del CS.
        
        print("DIRECCION = [", direccion, "] DATO = [", dato, "]")

    def recibir(self, direccion, dato='A'):
        """
        dato = A: Son los datos almacenados en la eeprom.
        dato = B: Son los datos del (ADC).
        """

        global ser

        flagMBS  = "+"
        flagLBS  = "-"

        QtCore.QCoreApplication.processEvents()

        TIEMPO_DATO = 0.035                         # Tiempo que le toma al CS 
                                                    # para guardar la informacion. 

        direccion_MSB = str(direccion >> 8)
        direccion_LSB = str(direccion & 0xFF)

        ser.write( bytes(direccion_MSB.encode()) )
        ser.write( bytes(flagMBS.encode()) )        # Direccion MSB.

        ser.write( bytes(direccion_LSB.encode()) )
        ser.write( bytes(flagLBS.encode()) )        # Direccion LSB.

        ser.write( bytes(dato.encode()) )           # Revisar en la documentacion las diferentes funciones.

        time.sleep(TIEMPO_DATO)                     # Tiempo del CS.

        try:
            bytesToRead = ser.in_waiting
            dato = ser.read(bytesToRead)
            dato = int(dato)

            print("DIRECCION = [", direccion, "] DATO = [", dato, "]")

            return dato

        except :

            print("DIRECCION = [", direccion, "] DATO = [", dato, "]")
            
            return 0        

    def seleccionoPuerto(self):
        """
        """

        comlist = serial.tools.list_ports.comports()
        puertos = []

        for element in comlist:
            puertos.append(element.device)

        print(puertos)

        return (puertos)

    def barraProgreso(self, progress, step):
        """
        """

        text_1 = "Paso [" + str(step) + "/5]"
        self.label_1.setText(text_1)

        self.progressBar.setValue(progress)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = PuertoSerie()
    window.show() 

    sys.exit(app.exec_())