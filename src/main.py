from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog
from PyQt5 import uic, QtCore

import sys

import numpy as np

import datetime

import os

from asistente.asistente import Asistente
from configuracion.configuracion import Configuracion
from copiar.copiar import Copiar
from tabla.tabla import Tabla
from puerto.puertoSerie import PuertoSerie
from configuracion.configuracion import ListaErrores

cs = {
    'CONFIGURACION': np.zeros((1, 1, 16)),
    'MONITOR'      : np.zeros((1, 1, 6)),
    'CALIBRACION'  : np.zeros((5, 1, 25)),
    'SERVICIOS'    : np.zeros((5, 1, 12)),
    'SOLDADURA'    : np.zeros((5, 255, 22)),
    'PROG_LISTA'   : [1],
    'DISP_LISTA'   : [1],
    'ETIQUETA'     : [""]    
}

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('main/guiMain.ui', self)

        # SETEO MATRIZ AL INICIO.
        self.seteoDicc()

        # OCULTAR.
        self.ocultar()

        self.caja_103.valueChanged.connect(self.ocultar)
        self.caja_109.valueChanged.connect(self.ocultar)
        self.caja_110.valueChanged.connect(self.ocultar)
        self.caja_113.valueChanged.connect(self.ocultar)
        self.caja_115.valueChanged.connect(self.ocultar)       

        # BLOQUEAR.
        self.bloquear()
        self.caja_1.valueChanged.connect(self.bloquear)
        self.caja_2.valueChanged.connect(self.bloquear)
        self.caja_209.valueChanged.connect(self.bloquear)

        # ACTUALIZO CAJAS.
        self.caja_1.valueChanged.connect(self.seteoCajas)
        self.caja_2.valueChanged.connect(self.seteoCajas)

        # ACTUALIZO DICCIONARIO.
        self.caja_100.valueChanged.connect(self.valorCajas)
        self.caja_101.valueChanged.connect(self.valorCajas)
        self.caja_102.valueChanged.connect(self.valorCajas)
        self.caja_103.valueChanged.connect(self.valorCajas)
        self.caja_104.valueChanged.connect(self.valorCajas)
        self.caja_105.valueChanged.connect(self.valorCajas)
        self.caja_106.valueChanged.connect(self.valorCajas)
        self.caja_107.valueChanged.connect(self.valorCajas)
        self.caja_108.valueChanged.connect(self.valorCajas)
        self.caja_109.valueChanged.connect(self.valorCajas)
        self.caja_110.valueChanged.connect(self.valorCajas)
        self.caja_111.valueChanged.connect(self.valorCajas)
        self.caja_112.valueChanged.connect(self.valorCajas)
        self.caja_113.valueChanged.connect(self.valorCajas)
        self.caja_114.valueChanged.connect(self.valorCajas)
        self.caja_115.valueChanged.connect(self.valorCajas)
        self.caja_116.valueChanged.connect(self.valorCajas)
        self.caja_117.valueChanged.connect(self.valorCajas)
        self.caja_118.valueChanged.connect(self.valorCajas)

        self.caja_200.valueChanged.connect(self.valorCajas)
        self.caja_201.valueChanged.connect(self.valorCajas)
        self.caja_202.valueChanged.connect(self.valorCajas)
        self.caja_203.valueChanged.connect(self.valorCajas)
        self.caja_204.valueChanged.connect(self.valorCajas)
        self.caja_205.valueChanged.connect(self.valorCajas)
        self.caja_206.valueChanged.connect(self.valorCajas)
        self.caja_207.valueChanged.connect(self.valorCajas)
        self.caja_208.valueChanged.connect(self.valorCajas)
        self.caja_209.valueChanged.connect(self.valorCajas)
        self.caja_210.valueChanged.connect(self.valorCajas)
        self.caja_211.valueChanged.connect(self.valorCajas)

        self.caja_300.valueChanged.connect(self.valorCajas)
        self.caja_301.valueChanged.connect(self.valorCajas)
        self.caja_302.valueChanged.connect(self.valorCajas)
        self.caja_303.valueChanged.connect(self.valorCajas)
        self.caja_304.valueChanged.connect(self.valorCajas)
        self.caja_305.valueChanged.connect(self.valorCajas)
        self.caja_306.valueChanged.connect(self.valorCajas)
        self.caja_307.valueChanged.connect(self.valorCajas)
        self.caja_308.valueChanged.connect(self.valorCajas)
        self.caja_309.valueChanged.connect(self.valorCajas)
        self.caja_310.valueChanged.connect(self.valorCajas)
        self.caja_311.valueChanged.connect(self.valorCajas)

        self.caja_400.valueChanged.connect(self.valorCajas)
        self.caja_401.valueChanged.connect(self.valorCajas)
        self.caja_402.valueChanged.connect(self.valorCajas)
        self.caja_403.valueChanged.connect(self.valorCajas)
        self.caja_404.valueChanged.connect(self.valorCajas)
        self.caja_405.valueChanged.connect(self.valorCajas)
        self.caja_406.valueChanged.connect(self.valorCajas)
        self.caja_407.valueChanged.connect(self.valorCajas)
        self.caja_408.valueChanged.connect(self.valorCajas)
        self.caja_409.valueChanged.connect(self.valorCajas)
        self.caja_410.valueChanged.connect(self.valorCajas)
        self.caja_411.valueChanged.connect(self.valorCajas)
        self.caja_412.valueChanged.connect(self.valorCajas)
        self.caja_413.valueChanged.connect(self.valorCajas)
        self.caja_414.valueChanged.connect(self.valorCajas)
        self.caja_415.valueChanged.connect(self.valorCajas)
        self.caja_416.valueChanged.connect(self.valorCajas)
        self.caja_417.valueChanged.connect(self.valorCajas)
        self.caja_418.valueChanged.connect(self.valorCajas)
        self.caja_419.valueChanged.connect(self.valorCajas)
        self.caja_420.valueChanged.connect(self.valorCajas)
        self.caja_421.valueChanged.connect(self.valorCajas)
        self.caja_422.valueChanged.connect(self.valorCajas)
        self.caja_423.valueChanged.connect(self.valorCajas)
        self.caja_424.valueChanged.connect(self.valorCajas)

        # MENU.
        self.actionAsistente.triggered.connect(self.ventanaAsistente)
        self.actionConfiguracion.triggered.connect(self.ventanaConfiguracion)
        self.actionCopiar.triggered.connect(self.ventanaCopiar)
        self.actionTabla.triggered.connect(self.ventanaTabla)

        # CS-PC.
        self.actionCS_PC.triggered.connect(self.CS_PC)
        self.actionPC_CS.triggered.connect(self.PC_CS)

        # MEDIR.
        self.btn_400.clicked.connect( lambda: self.medirCalibracion("Fuerza", self.caja_405.value()) )
        self.btn_401.clicked.connect( lambda: self.medirCalibracion("Fuerza", self.caja_406.value()) )
        self.btn_402.clicked.connect( lambda: self.medirCalibracion("Fuerza", self.caja_407.value()) )
        self.btn_403.clicked.connect( lambda: self.medirCalibracion("Fuerza", self.caja_408.value()) )
        self.btn_404.clicked.connect( lambda: self.medirCalibracion("Fuerza", self.caja_409.value()) )

        self.btn_405.clicked.connect( lambda: self.medirCalibracion("Intensidad", self.caja_415.value()) )
        self.btn_406.clicked.connect( lambda: self.medirCalibracion("Intensidad", self.caja_416.value()) )
        self.btn_407.clicked.connect( lambda: self.medirCalibracion("Intensidad", self.caja_417.value()) )
        self.btn_408.clicked.connect( lambda: self.medirCalibracion("Intensidad", self.caja_418.value()) )
        self.btn_409.clicked.connect( lambda: self.medirCalibracion("Intensidad", self.caja_419.value()) )

        # MONITOR.        
        self.actionFuerzaa.triggered.connect( lambda: self.monitor("Fuerza") )
        self.actionIntensidad.triggered.connect( lambda: self.monitor("Intensidad") )

        # CARGAR y GUARDAR.
        self.actionGuardar_Como.triggered.connect(self.guardar)
        self.actionAbrir.triggered.connect(self.cargar)

        # LISTA DE ERRORES.
        self.actionErrores.triggered.connect(lambda: window_6.show())

    def PC_CS(self):
        """
        """        

        pregunta = QMessageBox.question(self, 
                                        "Atencion", 
                                        "¿Desea Continuar?", 
                                        QMessageBox.Ok | QMessageBox.Cancel | QMessageBox.Reset
                                       )

        self.valorCajas()

        if pregunta == QMessageBox.Ok:
            #mando el diccionario. 

            self.pidoDatosConfiguracion()  
            self.pidoDatosTabla()

            dispActual = self.caja_1.value() - 1
            progActual = self.caja_2.value() - 1    

            puerto.show()
            #window_3.setearPuerto(puerto.seleccionoPuerto()) # bug en potencia.
            selecPort = window_3.seleccionarPuerto()
            puerto.confPuerto(selecPort, "OPEN")

            puerto.enviarDatosConfiguracion(cs)
            puerto.enviarDatosMonitor(cs, dispActual)

            for i in range(0, len(cs['DISP_LISTA'])):
                dispActual = cs['DISP_LISTA'][i] - 1
                progActual = cs['PROG_LISTA'][i] - 1               
            
                puerto.enviarDatosCalibracion(cs, dispActual)
                puerto.enviarDatosServicios(cs, dispActual)
                puerto.enviarDatosSoldadura(cs, dispActual, progActual)

            puerto.confPuerto(selecPort, "CLOSE")            
            puerto.hide()

        elif pregunta == QMessageBox.Reset:
            #mando uno vacio.
            
            puerto.show()
            window_3.setearPuerto(puerto.seleccionoPuerto())
            selecPort = window_3.seleccionarPuerto()
            puerto.confPuerto(selecPort, "OPEN")

            puerto.bloquearProgramas()
            #puerto.borrarEeprom()

            puerto.confPuerto(selecPort, "CLOSE")            
            puerto.hide()
            pass

        else:
            #no se hace nada.
            pass

    def CS_PC(self):
        """
        """

        pregunta = QMessageBox.question(self, 
                                        "Atencion", 
                                        "¿Desea Continuar?", 
                                        QMessageBox.Ok | QMessageBox.Cancel
                                       )

        self.valorCajas()

        if pregunta == QMessageBox.Ok:
            #recibo el diccionario.

            self.pidoDatosConfiguracion()  

            dispActual = self.caja_1.value() - 1
            progActual = self.caja_2.value() - 1

            puerto.show()
            #window_3.setearPuerto(puerto.seleccionoPuerto()) # bug en potencia.
            selecPort = window_3.seleccionarPuerto()
            puerto.confPuerto(selecPort, "OPEN")   

            cs['CONFIGURACION'] = puerto.recibirDatosConfiguracion(cs)
            cs['MONITOR'] = puerto.recibirDatosMonitor(cs, dispActual)
            
            for i in range(0, len(cs['DISP_LISTA'])):
                dispActual = cs['DISP_LISTA'][i] - 1
                progActual = cs['PROG_LISTA'][i] - 1   

                cs['CALIBRACION'] = puerto.recibirDatosCalibracion(cs, dispActual)
                cs['SERVICIOS'] = puerto.recibirDatosServicios(cs, dispActual)
                cs['SOLDADURA'] = puerto.recibirDatosSoldadura(cs, dispActual, progActual)

            puerto.confPuerto(selecPort, "CLOSE")            
            puerto.hide()       

            window_3.cargoConfiguracion(cs)
            window_5.cargoTabla(cs)         

        else:
            #no se hace nada.
            pass
        
        self.seteoCajas()

    def medirCalibracion(self, modo, dato):
        """
        """

        pregunta = QMessageBox.question(self, 
                                        "Atencion", 
                                        "¿Desea Continuar?", 
                                        QMessageBox.Ok | QMessageBox.Cancel
                                       )

        self.valorCajas()

        if pregunta == QMessageBox.Ok:
            #mando el diccionario. 

            dispActual = self.caja_1.value() - 1
            #progActual = self.caja_2.value() - 1 

            puerto.show()
            #window_3.setearPuerto(puerto.seleccionoPuerto()) # bug en potencia.
            selecPort = window_3.seleccionarPuerto()
            puerto.confPuerto(selecPort, "OPEN")

            puerto.enviarDatosCalibracion(cs, dispActual)

            if modo == "Fuerza":
                puerto.medirFuerza(cs, dispActual, dato)

            elif modo == "Intensidad":
                puerto.medirIntensidad(cs, dispActual, dato)

            else:
                pass

            puerto.confPuerto(selecPort, "CLOSE")   
            puerto.hide()

        elif pregunta == QMessageBox.Reset:
            #mando uno vacio.
            pass

        else:
            #no se hace nada.
            pass     

    def monitor(self, modo):
        """
        """
        
        pregunta = QMessageBox.question(self, 
                                        "Atencion", 
                                        "¿Desea Continuar?", 
                                        QMessageBox.Ok | QMessageBox.Cancel
                                       )

        self.valorCajas()

        if pregunta == QMessageBox.Ok:
            #mando el diccionario. 

            dispActual = self.caja_1.value() - 1
            #progActual = self.caja_2.value() - 1 

            puerto.show()
            #window_3.setearPuerto(puerto.seleccionoPuerto()) # bug en potencia.
            selecPort = window_3.seleccionarPuerto()
            puerto.confPuerto(selecPort, "OPEN")

            puerto.enviarDatosMonitor(cs, dispActual)

            if modo == "Fuerza":
                puerto.monitorFuerza()

            elif modo == "Intensidad":
                puerto.monitorIntensidad()

            else:
                pass

            puerto.confPuerto(selecPort, "CLOSE")   
            puerto.hide()

        elif pregunta == QMessageBox.Reset:
            #mando uno vacio.
            pass

        else:
            #no se hace nada.
            pass

    def pidoDatosAsistente(self):
        """
        """        

        valor = window_2.datosAsistente()

        dispositivo = self.caja_1.value() - 1
        programa = valor[0] - 1

        cs['SOLDADURA'][dispositivo, programa, 6] = valor[1] 
        cs['SOLDADURA'][dispositivo, programa, 7] = valor[2] 
        cs['SOLDADURA'][dispositivo, programa, 18] = valor[3] * 100

        self.seteoCajas()

    def pidoDatosConfiguracion(self):
        """
        """

        valor = window_3.datosConfiguracion()

        disp = self.caja_1.value() 
        prog = self.caja_2.value() 

        if self.caja_102.value() == 0:
            cs['CONFIGURACION'][0][0][0] = valor[0]
        else:
            cs['CONFIGURACION'][0][0][0] = 20

        #cs['CONFIGURACION'][0][0][0] = valor[0]
        cs['CONFIGURACION'][0][0][1] = valor[1]
        cs['CONFIGURACION'][0][0][2] = valor[2]
        cs['CONFIGURACION'][0][0][3] = valor[3]

        cs['CONFIGURACION'][0][0][4] = disp
        cs['CONFIGURACION'][0][0][5] = prog

    def pidoDatosCopiar(self):
        """
        """
        
        cs['SOLDADURA'] = window_4.identifico(cs['SOLDADURA'])

    def pidoDatosTabla(self):
        """
        """
        
        valor = window_5.datosTabla()

        cs['PROG_LISTA'] = valor[0]
        cs['DISP_LISTA'] = valor[1]

        largo = len(valor[0])
        for i in range(0 , largo):
            disp = valor[1][i] - 1 
            prog = valor[0][i] - 1 

            cs['SOLDADURA'][disp][prog][21] = valor[2][i]

        cs['ETIQUETA'] = valor[3]

        self.bloquear()

    def valorCajas(self):
        """
        Esta funcion actualiza los valores de la matriz. Se utiliza cuando las cajas cambian
        su valor y cuando caja_1 y caja_2 cambian. Ademas se usa en PC -> CS
        """

        dato_1 = cs['SOLDADURA'].copy()
        dato_2 = cs['SERVICIOS'].copy()
        dato_3 = cs['MONITOR'].copy()
        dato_4 = cs['CALIBRACION'].copy()    

        disp = self.caja_1.value() - 1
        prog = self.caja_2.value() - 1

        #SOLDADURA
        dato_1[disp][prog][0] = self.caja_100.value()
        dato_1[disp][prog][1] = self.caja_101.value()
        dato_1[disp][prog][2] = self.caja_102.value()
        dato_1[disp][prog][3] = self.caja_103.value()
        dato_1[disp][prog][4] = self.caja_104.value()
        dato_1[disp][prog][5] = self.caja_105.value()
        dato_1[disp][prog][6] = self.caja_106.value()
        dato_1[disp][prog][7] = self.caja_107.value()
        dato_1[disp][prog][8] = self.caja_108.value()
        dato_1[disp][prog][9] = self.caja_109.value()
        dato_1[disp][prog][10] = self.caja_110.value()
        dato_1[disp][prog][11] = self.caja_111.value()
        dato_1[disp][prog][12] = self.caja_112.value()
        dato_1[disp][prog][13] = self.caja_113.value()
        dato_1[disp][prog][14] = self.caja_114.value()
        dato_1[disp][prog][15] = self.caja_115.value()
        dato_1[disp][prog][16] = self.caja_116.value()
        dato_1[disp][prog][17] = self.caja_117.value()
        dato_1[disp][prog][18] = self.caja_118.value()

        #SERVICIOS
        dato_2[disp][0][0] = self.caja_200.value()
        dato_2[disp][0][1] = self.caja_201.value()
        dato_2[disp][0][2] = self.caja_202.value()
        dato_2[disp][0][3] = self.caja_203.value()
        dato_2[disp][0][4] = self.caja_204.value()
        dato_2[disp][0][5] = self.caja_205.value()
        dato_2[disp][0][6] = self.caja_206.value()
        dato_2[disp][0][7] = self.caja_207.value()
        dato_2[disp][0][8] = self.caja_208.value()
        dato_2[disp][0][9] = self.caja_209.value()
        dato_2[disp][0][10] = self.caja_210.value()
        dato_2[disp][0][11] = self.caja_211.value()

        #MONITOR
        dato_3[0][0][0] = self.caja_300.value()
        dato_3[0][0][1] = self.caja_301.value()
        dato_3[0][0][2] = self.caja_308.value()
        dato_3[0][0][3] = self.caja_309.value()
        dato_3[0][0][4] = self.caja_304.value()
        dato_3[0][0][5] = self.caja_305.value()

        #CALIBRACION
        dato_4[disp][0][0] = self.caja_400.value()
        dato_4[disp][0][1] = self.caja_401.value()
        dato_4[disp][0][2] = self.caja_402.value()
        dato_4[disp][0][3] = self.caja_403.value()
        dato_4[disp][0][4] = self.caja_404.value()
        dato_4[disp][0][5] = self.caja_405.value()
        dato_4[disp][0][6] = self.caja_406.value()
        dato_4[disp][0][7] = self.caja_407.value()
        dato_4[disp][0][8] = self.caja_408.value()
        dato_4[disp][0][9] = self.caja_409.value()
        dato_4[disp][0][10] = self.caja_410.value()
        dato_4[disp][0][11] = self.caja_411.value()
        dato_4[disp][0][12] = self.caja_412.value()
        dato_4[disp][0][13] = self.caja_413.value()
        dato_4[disp][0][14] = self.caja_414.value()
        dato_4[disp][0][15] = self.caja_415.value()
        dato_4[disp][0][16] = self.caja_416.value()
        dato_4[disp][0][17] = self.caja_417.value()
        dato_4[disp][0][18] = self.caja_418.value()
        dato_4[disp][0][19] = self.caja_419.value()
        dato_4[disp][0][20] = self.caja_420.value()
        dato_4[disp][0][21] = self.caja_421.value()
        dato_4[disp][0][22] = self.caja_422.value()
        dato_4[disp][0][23] = self.caja_423.value()
        dato_4[disp][0][24] = self.caja_424.value()

        cs['SOLDADURA'] = dato_1
        cs['SERVICIOS'] = dato_2
        cs['MONITOR'] = dato_3
        cs['CALIBRACION'] = dato_4

    def seteoCajas(self):
        """
        Actualizo los valores de las cajas cuando CS -> PC, o cargo un archivo.
        """

        self.bloqueoSignals(True)        

        dato_1 = cs['SOLDADURA'].copy()
        dato_2 = cs['SERVICIOS'].copy()
        dato_3 = cs['MONITOR'].copy()
        dato_4 = cs['CALIBRACION'].copy()     

        disp = self.caja_1.value() - 1
        prog = self.caja_2.value() - 1

        #SOLDADURA
        self.caja_100.setValue(dato_1[disp][prog][0])
        self.caja_101.setValue(dato_1[disp][prog][1])
        self.caja_102.setValue(dato_1[disp][prog][2])
        self.caja_103.setValue(dato_1[disp][prog][3])
        self.caja_104.setValue(dato_1[disp][prog][4])
        self.caja_105.setValue(dato_1[disp][prog][5])
        self.caja_106.setValue(dato_1[disp][prog][6])
        self.caja_107.setValue(dato_1[disp][prog][7])
        self.caja_108.setValue(dato_1[disp][prog][8])
        self.caja_109.setValue(dato_1[disp][prog][9])
        self.caja_110.setValue(dato_1[disp][prog][10])
        self.caja_111.setValue(dato_1[disp][prog][11])
        self.caja_112.setValue(dato_1[disp][prog][12])
        self.caja_113.setValue(dato_1[disp][prog][13])
        self.caja_114.setValue(dato_1[disp][prog][14])
        self.caja_115.setValue(dato_1[disp][prog][15])
        self.caja_116.setValue(dato_1[disp][prog][16])
        self.caja_117.setValue(dato_1[disp][prog][17])
        self.caja_118.setValue(dato_1[disp][prog][18])

        #SERVICIOS
        self.caja_200.setValue(dato_2[disp][0][0])
        self.caja_201.setValue(dato_2[disp][0][1])
        self.caja_202.setValue(dato_2[disp][0][2])
        self.caja_203.setValue(dato_2[disp][0][3])
        self.caja_204.setValue(dato_2[disp][0][4])
        self.caja_205.setValue(dato_2[disp][0][5])
        self.caja_206.setValue(dato_2[disp][0][6])
        self.caja_207.setValue(dato_2[disp][0][7])
        self.caja_208.setValue(dato_2[disp][0][8])
        self.caja_209.setValue(dato_2[disp][0][9])
        self.caja_210.setValue(dato_2[disp][0][10])
        self.caja_211.setValue(dato_2[disp][0][11])

        #MONITOR
        self.caja_300.setValue(dato_3[0][0][0])
        self.caja_301.setValue(dato_3[0][0][1])
        self.caja_308.setValue(dato_3[0][0][2])
        self.caja_309.setValue(dato_3[0][0][3])
        self.caja_304.setValue(dato_3[0][0][4])
        self.caja_305.setValue(dato_3[0][0][5])

        #CALIBRACION
        self.caja_400.setValue(dato_4[disp][0][0])
        self.caja_401.setValue(dato_4[disp][0][1])
        self.caja_402.setValue(dato_4[disp][0][2])
        self.caja_403.setValue(dato_4[disp][0][3])
        self.caja_404.setValue(dato_4[disp][0][4])
        self.caja_405.setValue(dato_4[disp][0][5])
        self.caja_406.setValue(dato_4[disp][0][6])
        self.caja_407.setValue(dato_4[disp][0][7])
        self.caja_408.setValue(dato_4[disp][0][8])
        self.caja_409.setValue(dato_4[disp][0][9])
        self.caja_410.setValue(dato_4[disp][0][10])
        self.caja_411.setValue(dato_4[disp][0][11])
        self.caja_412.setValue(dato_4[disp][0][12])
        self.caja_413.setValue(dato_4[disp][0][13])
        self.caja_414.setValue(dato_4[disp][0][14])
        self.caja_415.setValue(dato_4[disp][0][15])
        self.caja_416.setValue(dato_4[disp][0][16])
        self.caja_417.setValue(dato_4[disp][0][17])
        self.caja_418.setValue(dato_4[disp][0][18])
        self.caja_419.setValue(dato_4[disp][0][19])
        self.caja_420.setValue(dato_4[disp][0][20])
        self.caja_421.setValue(dato_4[disp][0][21])
        self.caja_422.setValue(dato_4[disp][0][22])
        self.caja_423.setValue(dato_4[disp][0][23])
        self.caja_424.setValue(dato_4[disp][0][24])

        self.bloqueoSignals(False)
        self.ocultar()

    def seteoDicc(self):
        """
        Actualizo el diccionario al iniciar el programa
        """

        dato_1 = cs['SOLDADURA'].copy()
        dato_2 = cs['SERVICIOS'].copy()
        dato_3 = cs['MONITOR'].copy()
        dato_4 = cs['CALIBRACION'].copy()    

        #SOLDADURA
        dato_1[ : , : , 0] = self.caja_100.value()
        dato_1[ : , : , 1] = self.caja_101.value()
        dato_1[ : , : , 2] = self.caja_102.value()
        dato_1[ : , : , 3] = self.caja_103.value()
        dato_1[ : , : , 4] = self.caja_104.value()
        dato_1[ : , : , 5] = self.caja_105.value()
        dato_1[ : , : , 6] = self.caja_106.value()
        dato_1[ : , : , 7] = self.caja_107.value()
        dato_1[ : , : , 8] = self.caja_108.value()
        dato_1[ : , : , 9] = self.caja_109.value()
        dato_1[ : , : , 10] = self.caja_110.value()
        dato_1[ : , : , 11] = self.caja_111.value()
        dato_1[ : , : , 12] = self.caja_112.value()
        dato_1[ : , : , 13] = self.caja_113.value()
        dato_1[ : , : , 14] = self.caja_114.value()
        dato_1[ : , : , 15] = self.caja_115.value()
        dato_1[ : , : , 16] = self.caja_116.value()
        dato_1[ : , : , 17] = self.caja_117.value()
        dato_1[ : , : , 18] = self.caja_118.value()

        #SERVICIOS
        dato_2[ : , : , 0] = self.caja_200.value()
        dato_2[ : , : , 1] = self.caja_201.value()
        dato_2[ : , : , 2] = self.caja_202.value()
        dato_2[ : , : , 3] = self.caja_203.value()
        dato_2[ : , : , 4] = self.caja_204.value()
        dato_2[ : , : , 5] = self.caja_205.value()
        dato_2[ : , : , 6] = self.caja_206.value()
        dato_2[ : , : , 7] = self.caja_207.value()
        dato_2[ : , : , 8] = self.caja_208.value()
        dato_2[ : , : , 9] = self.caja_209.value()
        dato_2[ : , : , 10] = self.caja_210.value()
        dato_2[ : , : , 11] = self.caja_211.value()

        #MONITOR
        dato_3[ : , : , 0] = self.caja_300.value()
        dato_3[ : , : , 1] = self.caja_301.value()
        dato_3[ : , : , 2] = self.caja_308.value()
        dato_3[ : , : , 3] = self.caja_309.value()
        dato_3[ : , : , 4] = self.caja_304.value()
        dato_3[ : , : , 5] = self.caja_305.value()

        #CALIBRACION
        dato_4[ : , : , 0] = self.caja_400.value()
        dato_4[ : , : , 1] = self.caja_401.value()
        dato_4[ : , : , 2] = self.caja_402.value()
        dato_4[ : , : , 3] = self.caja_403.value()
        dato_4[ : , : , 4] = self.caja_404.value()
        dato_4[ : , : , 5] = self.caja_405.value()
        dato_4[ : , : , 6] = self.caja_406.value()
        dato_4[ : , : , 7] = self.caja_407.value()
        dato_4[ : , : , 8] = self.caja_408.value()
        dato_4[ : , : , 9] = self.caja_409.value()
        dato_4[ : , : , 10] = self.caja_410.value()
        dato_4[ : , : , 11] = self.caja_411.value()
        dato_4[ : , : , 12] = self.caja_412.value()
        dato_4[ : , : , 13] = self.caja_413.value()
        dato_4[ : , : , 14] = self.caja_414.value()
        dato_4[ : , : , 15] = self.caja_415.value()
        dato_4[ : , : , 16] = self.caja_416.value()
        dato_4[ : , : , 17] = self.caja_417.value()
        dato_4[ : , : , 18] = self.caja_418.value()
        dato_4[ : , : , 19] = self.caja_419.value()
        dato_4[ : , : , 20] = self.caja_420.value()
        dato_4[ : , : , 21] = self.caja_421.value()
        dato_4[ : , : , 22] = self.caja_422.value()
        dato_4[ : , : , 23] = self.caja_423.value()
        dato_4[ : , : , 24] = self.caja_424.value()

        cs['SOLDADURA'] = dato_1
        cs['SERVICIOS'] = dato_2
        cs['MONITOR'] = dato_3
        cs['CALIBRACION'] = dato_4

    def bloqueoSignals(self, estado):
        """
        Esta funcion bloquea las señales cuenado cuando cambio los valores de las cajas.

        estado = True o False
        """

        #SOLDADURA
        self.caja_100.blockSignals(estado)
        self.caja_101.blockSignals(estado)
        self.caja_102.blockSignals(estado)
        self.caja_103.blockSignals(estado)
        self.caja_104.blockSignals(estado)
        self.caja_105.blockSignals(estado)
        self.caja_106.blockSignals(estado)
        self.caja_107.blockSignals(estado)
        self.caja_108.blockSignals(estado)
        self.caja_109.blockSignals(estado)
        self.caja_110.blockSignals(estado)
        self.caja_111.blockSignals(estado)
        self.caja_112.blockSignals(estado)
        self.caja_113.blockSignals(estado)
        self.caja_114.blockSignals(estado)
        self.caja_115.blockSignals(estado)
        self.caja_116.blockSignals(estado)
        self.caja_117.blockSignals(estado)
        self.caja_118.blockSignals(estado)

        #SERVICIOS
        self.caja_200.blockSignals(estado)
        self.caja_201.blockSignals(estado)
        self.caja_202.blockSignals(estado)
        self.caja_203.blockSignals(estado)
        self.caja_204.blockSignals(estado)
        self.caja_205.blockSignals(estado)
        self.caja_206.blockSignals(estado)
        self.caja_207.blockSignals(estado)
        self.caja_208.blockSignals(estado)
        self.caja_209.blockSignals(estado)
        self.caja_210.blockSignals(estado)
        self.caja_211.blockSignals(estado)

        #MONITOR
        self.caja_300.blockSignals(estado)
        self.caja_301.blockSignals(estado)
        self.caja_302.blockSignals(estado)
        self.caja_303.blockSignals(estado)
        self.caja_304.blockSignals(estado)
        self.caja_305.blockSignals(estado)
        self.caja_306.blockSignals(estado)
        self.caja_307.blockSignals(estado)
        self.caja_308.blockSignals(estado)
        self.caja_309.blockSignals(estado)
        self.caja_310.blockSignals(estado)
        self.caja_311.blockSignals(estado)

        #CALIBRACION
        self.caja_400.blockSignals(estado)
        self.caja_401.blockSignals(estado)
        self.caja_402.blockSignals(estado)
        self.caja_403.blockSignals(estado)
        self.caja_404.blockSignals(estado)
        self.caja_405.blockSignals(estado)
        self.caja_406.blockSignals(estado)
        self.caja_407.blockSignals(estado)
        self.caja_408.blockSignals(estado)
        self.caja_409.blockSignals(estado)
        self.caja_410.blockSignals(estado)
        self.caja_411.blockSignals(estado)
        self.caja_412.blockSignals(estado)
        self.caja_413.blockSignals(estado)
        self.caja_414.blockSignals(estado)
        self.caja_415.blockSignals(estado)
        self.caja_416.blockSignals(estado)
        self.caja_417.blockSignals(estado)
        self.caja_418.blockSignals(estado)
        self.caja_419.blockSignals(estado)
        self.caja_420.blockSignals(estado)
        self.caja_421.blockSignals(estado)
        self.caja_422.blockSignals(estado)
        self.caja_423.blockSignals(estado)
        self.caja_424.blockSignals(estado)

    def bloquear(self):
        """
        Bloqueo los programas que no estan definidos en la tabla

        estado = False (disabled)
        estado = True  (enabled)
        """
        
        dispositivo = self.caja_1.value()
        programa = self.caja_2.value()
        estado = False

        if self.caja_209.value() == 0:
            self.caja_206.setValue(0)
            self.caja_206.setEnabled(False)
        else:
            aux = self.caja_206.value()
            self.caja_206.setValue(aux)
            self.caja_206.setEnabled(True)

        largo = len(cs["DISP_LISTA"])
        for i in range(0, largo):  
            if( (dispositivo == cs['DISP_LISTA'][i]) and (programa == cs['PROG_LISTA'][i]) ):
                estado = True
                break
            else:
                estado = False

        self.frame_100.setEnabled(estado)

    def ocultar(self):
        """
        Sirve para ocultar caja que no se utilizan.
        """
        
        if(self.caja_103.value() == 0):
            self.caja_104.hide()
            self.caja_105.hide()

            self.lbl_108.hide()
            self.lbl_109.hide()
            self.lbl_110.hide()
            self.lbl_111.hide()
        else:
            self.caja_104.show()
            self.caja_105.show()

            self.lbl_108.show()
            self.lbl_109.show()
            self.lbl_110.show()
            self.lbl_111.show()

        if(self.caja_109.value() == 1):
            self.caja_108.hide()

            self.lbl_116.hide()
            self.lbl_117.hide()
        else:
            self.caja_108.show()

            self.lbl_116.show()
            self.lbl_117.show()

        if(self.caja_110.value() == 0):
            self.caja_111.hide()
            self.caja_112.hide()

            self.lbl_121.hide()
            self.lbl_122.hide()
            self.lbl_123.hide()
            self.lbl_124.hide()
        else:
            self.caja_111.show()
            self.caja_112.show()

            self.lbl_121.show()
            self.lbl_122.show()
            self.lbl_123.show()
            self.lbl_124.show()

        if(self.caja_113.value() == 0):
            self.caja_114.hide()

            self.lbl_127.hide()
            self.lbl_128.hide()
        else:
            self.caja_114.show()

            self.lbl_127.show()
            self.lbl_128.show()

        if(self.caja_115.value() == 0):
            self.caja_116.hide()

            self.lbl_131.hide()
            self.lbl_132.hide()
        else:
            self.caja_116.show()

            self.lbl_131.show()
            self.lbl_132.show()

    def ventanaAsistente(self):
        window_2.show()

    def ventanaConfiguracion(self):
        window_3.show()

        window_3.setearPuerto(puerto.seleccionoPuerto())

    def ventanaCopiar(self):
        window_4.show()

    def ventanaTabla(self):
        window_5.show()

    def guardar(self):
        """
        """

        self.pidoDatosConfiguracion()
        self.valorCajas()

        os.chdir(os.path.expanduser("~"))

        fecha = str(datetime.datetime.now().date())
        nombre_archivo = ("save_" + fecha + ".npy") 

        try:
            direccion = QFileDialog.getSaveFileName(self, "Guardar", nombre_archivo)
            direccion = direccion[0]
            np.save(direccion, cs)

        except:
            pass

    def cargar(self):
        """
        """

        os.chdir(os.path.expanduser("~"))

        try:
            direccion = QFileDialog.getOpenFileName(self, "Abrir", "", "*.npy")
            direccion = direccion[0]
            filename = np.load(direccion, allow_pickle=True)
            
            cs['CONFIGURACION'] = filename.item().get("CONFIGURACION")
            cs['MONITOR'] = filename.item().get("MONITOR")
            cs['CALIBRACION'] = filename.item().get("CALIBRACION")
            cs['SERVICIOS'] = filename.item().get("SERVICIOS")
            cs['SOLDADURA'] = filename.item().get("SOLDADURA")
            cs['PROG_LISTA'] = filename.item().get("PROG_LISTA")
            cs['DISP_LISTA'] = filename.item().get("DISP_LISTA")
            cs['ETIQUETA'] = filename.item().get("ETIQUETA")
            
            window_3.cargoConfiguracion(cs)
            window_5.cargoTabla(cs)            
            self.seteoCajas()

        except:
            pass


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window_1 = Main()
    window_2 = Asistente()
    window_3 = Configuracion()
    window_4 = Copiar()
    window_5 = Tabla()
    window_6 = ListaErrores()

    puerto = PuertoSerie()

    window_1.show()
    #window_2.show()
    #window_3.show()
    #window_4.show()
    #window_5.show()
    
    window_2.buttonBox.accepted.connect(window_1.pidoDatosAsistente)
    window_4.buttonBox.accepted.connect(window_1.pidoDatosCopiar)
    window_5.buttonBox.accepted.connect(window_1.pidoDatosTabla)

    sys.exit(app.exec_())