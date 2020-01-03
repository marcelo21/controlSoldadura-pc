from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic, QtCore

import sys

import numpy as np

import serial

from numpy import polynomial as P

import time

import serial.tools.list_ports

ser = 0

class PuertoSerie(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi('puerto/guiEspere.ui', self)

    def conversorDuty(self, tension):
        """
        Tension -> Duty
        """

        x = np.array([10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,470,480,490,500,510,520,530,540,550,560,570,580,590,600,610,620,630,640,650,660,670,680,690,700,710,720,730,740,750,760,770,780,790,800,810,820,830,840,850,860,870,880,890,900,910,920,930,940,950,960,970,980,990])
        y = np.array([0.228,0.42,0.602,0.778,0.973,1.143,1.314,1.477,1.662,1.821,1.964,2.146,2.299,2.424,2.581,2.715,2.882,3.01,3.152,3.286,3.433,3.567,3.701,3.833,3.97,4.1,4.23,4.36,4.5,4.63,4.76,4.86,4.98,5.08,5.22,5.31,5.42,5.53,5.64,5.74,5.85,5.95,6.07,6.16,6.26,6.4,6.51,6.6,6.71,6.8,6.9,7.02,7.1,7.18,7.25,7.31,7.39,7.49,7.58,7.68,7.77,7.89,7.96,8.06,8.09,8.15,8.22,8.31,8.39,8.5,8.57,8.69,8.76,8.84,8.91,9,9.07,9.11,9.17,9.25,9.29,9.38,9.45,9.51,9.58,9.65,9.7,9.79,9.87,9.91,9.98,10.06,10.12,10.19,10.25,10.34,10.37,10.44,10.49])

        if(tension > 0):
            p = P.Polynomial.fit(y, x, 4)
            valor_1 = p(tension)

        else:
            valor_1 = 0

        return valor_1

    def conversorTension(self, fuerza, calibracion, dispActual):
        """
        Fuerza -> Tension
        """

        x = calibracion[dispActual, 0, 5:9 + 1]
        y = calibracion[dispActual, 0, 10:14 + 1]

        if(fuerza > 0):
            p = P.Polynomial.fit(y, x, 4)
            valor_1 = p(fuerza)
            valor_2 = self.conversorDuty(valor_1)

        else:
            valor_1 = 0
            valor_2 = 0

        valor_2 = int(round(valor_2))

        #print(x)
        #print(y)
        #print("Intensidad:", intensidad)
        #print("Porcentaje:", valor_1)
        #print("% CS:", valor_2)

        return valor_2

    def conversorPorcentaje(self, intensidad, calibracion, dispActual):
        """
        Intensidad -> Porcentaje
        """

        x = calibracion[dispActual, 0, 15:19 + 1]
        y = calibracion[dispActual, 0, 20:24 + 1]        

        if(intensidad > 0):
            p = P.Polynomial.fit(y, x, 4)
            valor_1 = p(intensidad)
            valor_2 = valor_1 * (7300 / 100)

        else:
            valor_1 = 0
            valor_2 = 0

        valor_2 = int(round(valor_2))

        #print(x)
        #print(y)
        #print("Intensidad:", intensidad)
        #print("Porcentaje:", valor_1)
        #print("% CS:", valor_2)

        return valor_2

    def borrarEeprom(self):
        """
        """

        dato = 255

        for i in range(0, 65535):
            self.barraProgreso( 100 * i / 65535 )
            self.enviar(i, dato)

    def bloquearProgramas(self):
        """
        """

        self.barraProgreso( 1 )

        D_INI_SOLD = 0x00B0

        dato = 255

        cont = 0

        for i in range(1, 4):

            dispActual = i

            for j in range(1, 255):

                progActual = j
                
                cont += 1
                
                D_POSC_MEM = ( ( 0x4020 * (dispActual - 0x0001) ) + ( 0x0040 * (progActual - 0x0001) ) )
                self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.

                self.barraProgreso(100 * cont / 1275)

    def enviarDatosConfiguracion(self, cs):
        """
        """

        self.barraProgreso(100 / 5 * 1)

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

    def enviarDatosMonitor(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 2)

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

    def enviarDatosCalibracion(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 3)

        D_INI_CALI = 0x0050
        D_POSC_MEM = ( 0x4020 * dispActual )

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

        # Offset Fuerza

        #dato = int(cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0023 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset fuerza.
        #self.enviar(0x0024 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset fuerza.  

        # Offset Intensidad   

        #dato = int(cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0025 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset intensidad.
        #self.enviar(0x0026 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset intensidad.  

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

        # Transformar offset fuerza -> duty / offset intensidad -> porcentaje

        #dato = int(cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x002D + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset fuerza.
        #self.enviar(0x002E + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset fuerza.  

        #dato = int(cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x002F + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset intensidad.
        #self.enviar(0x0030 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset intensidad.  

        # Aux sirve para la funcion medirCalibracion.

        #dato = self.conversorTension(cs['CALIBRACION'][dispActual][0][2], cs['CALIBRACION'], dispActual)
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0031 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # aux fuerza.
        #self.enviar(0x0032 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # aux fuerza.  

        #dato = self.conversorPorcentaje(cs['CALIBRACION'][dispActual][0][0], cs['CALIBRACION'], dispActual)
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.enviar(0x0033 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # aux intensidad.
        #self.enviar(0x0034 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # aux intensidad.  

    def enviarDatosServicios(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 4)

        D_INI_SERV = 0x0090
        D_POSC_MEM = ( 0x4020 * dispActual )

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

    def enviarDatosSoldadura(self, cs, dispActual, progActual):
        """
        """

        self.barraProgreso(100 / 5 * 5)

        print("- DISP:", dispActual + 1, "- PROG:", progActual + 1)

        D_INI_SOLD = 0x00B0
        D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )

        #################### PARAMETROS USUARIOS.

        # 1
    
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
        print("Tiempo Soldadura 2:", dato)

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

        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][4], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001B + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 1.
        self.enviar(0x001C + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 1.

        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][7], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x001D + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Intensidad 2.
        self.enviar(0x001E + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Intensidad 2.

        dato = self.conversorPorcentaje(cs['SOLDADURA'][dispActual][progActual][11], cs['CALIBRACION'], dispActual)
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

        dato = self.conversorTension(cs['SOLDADURA'][dispActual][progActual][18], cs['CALIBRACION'], dispActual)
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0025 + D_INI_SOLD + D_POSC_MEM, dato_MSB)              # Fuerza.
        self.enviar(0x0026 + D_INI_SOLD + D_POSC_MEM, dato_LSB)              # Fuerza.

        dato = int(cs['SOLDADURA'][dispActual][progActual][21])
        self.enviar(0x0027 + D_INI_SOLD + D_POSC_MEM, dato)                  # Comportamiento.

    def recibirDatosConfiguracion(self, cs):
        """
        """

        self.barraProgreso(100 / 5 * 1)

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

        dato = self.recibir(0x0004 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][4] = dato             # Disp. Actual.

        dato = self.recibir(0x0005 + D_INI_CONF)
        cs['CONFIGURACION'][0][0][5] = dato             # Prog. Actual.

        return cs['CONFIGURACION']

    def recibirDatosMonitor(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 2)

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

        return cs['MONITOR']

    def recibirDatosCalibracion(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 3)

        D_INI_CALI = 0x0050
        D_POSC_MEM = ( 0x4020 * dispActual )

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

        # Offset Fuerza

        #dato = cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.recibir(0x0023 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset fuerza.
        #self.recibir(0x0024 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset fuerza.  

        # Offset Intensidad   

        #dato = cs['CALIBRACION'][dispActual][0][0])
        #dato_MSB = dato >> 8
        #dato_LSB = dato & 0xFF
        #self.recibir(0x0025 + D_INI_CALI + D_POSC_MEM, dato_MSB)          # offset intensidad.
        #self.recibir(0x0026 + D_INI_CALI + D_POSC_MEM, dato_LSB)          # offset intensidad.  

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

        return cs['CALIBRACION']

    def recibirDatosServicios(self, cs, dispActual):
        """
        """

        self.barraProgreso(100 / 5 * 4)

        D_INI_SERV = 0x0090
        D_POSC_MEM = ( 0x4020 * dispActual )
        
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

        return cs['SERVICIOS']

    def recibirDatosSoldadura(self, cs, dispActual, progActual):
        """
        """

        self.barraProgreso(100 / 5 * 5)

        print("- DISP:", dispActual + 1, "- PROG:", progActual + 1)

        D_INI_SOLD = 0x00B0
        D_POSC_MEM = ( ( 0x4020 * dispActual ) + ( 0x0040 * progActual ) )

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

        return cs['SOLDADURA']

    def medirFuerza(self, cs, dispActual, dato):
        """
        """

        self.barraProgreso(100 / 5 * 3)

        D_INI_CALI = 0x0050
        D_POSC_MEM = 0x4020 * dispActual

        print("-Fuerza-")
        
        dato = int(self.conversorDuty(dato))
        dato_MSB = dato >> 8
        dato_LSB = dato & 0xFF
        self.enviar(0x0031 + D_INI_CALI + D_POSC_MEM, dato_MSB) # aux fuerza.
        self.enviar(0x0032 + D_INI_CALI + D_POSC_MEM, dato_LSB) # aux fuerza.         

        print("Dato:", dato)
        print("Dato_MSB:", dato_MSB)
        print("Dato_LSB:", dato_LSB)

        dato = "E"                                              # CS hay que calibrar. 
        ser.write( bytes(dato.encode()) )                       # Envio bandera calibracion.

        self.barraProgreso(100)

    def medirIntensidad(self, cs, dispActual, dato):
        """
        """

        self.barraProgreso(100 / 5 * 3)

        D_INI_CALI = 0x0050
        D_POSC_MEM = 0x4020 * dispActual

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

        self.barraProgreso(100)

    def monitorFuerza(self, cs, dispActual):
        """
        """

        pass

    def monitorIntensidad(self, cs, dispActual):
        """
        """

        pass

    def confPuerto(self, puerto, estado):
        """
        estado = "OPEN"
        estado = "CLOSE"
        """

        global ser

        TIEMPO_CONEXION = 0.025                                 # Tiempo para habilitar la conexion.
        VELOCIDAD = 9600                                        # Velocidad del puerto.

        if(estado == "OPEN"):
            ser = serial.Serial(puerto, baudrate=VELOCIDAD)    # Configuro el puerto.
            time.sleep(TIEMPO_CONEXION)                        # Retardo para establecer 
                                                               # la conexión serial.
            
            ser.flushInput()                                   # Limpio la entrada.
            ser.flushOutput()                                  # Limpio la salida.

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

        TIEMPO_DATO = 0.030                         # Tiempo que le toma al CS 
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

    def recibir(self, direccion):
        """
        """

        global ser

        flagMBS  = "+"
        flagLBS  = "-"

        QtCore.QCoreApplication.processEvents()

        TIEMPO_DATO = 0.030                         # Tiempo que le toma al CS 
                                                    # para guardar la informacion.  

        direccion_MSB = str(direccion >> 8)
        direccion_LSB = str(direccion & 0xFF)
        dato = "A"                                  # Le aviso al CS que hay que leer.

        ser.write( bytes(direccion_MSB.encode()) )
        ser.write( bytes(flagMBS.encode()) )        # Direccion MSB.

        ser.write( bytes(direccion_LSB.encode()) )
        ser.write( bytes(flagLBS.encode()) )        # Direccion LSB.

        ser.write( bytes(dato.encode()) )

        time.sleep(TIEMPO_DATO)                     # Tiempo del CS.

        try:
            bytesToRead = ser.inWaiting()
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

    def barraProgreso(self, valor):
        """
        """

        self.progressBar.setValue(valor)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = PuertoSerie()
    window.show()

    sys.exit(app.exec_())