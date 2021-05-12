from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog
from PyQt5 import uic, QtCore

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

import os
import sys
import datetime

import numpy as np
import pandas as pd

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
    'SOLDADURA'    : np.zeros((5, 255, 24)),    #Antes --- 'SOLDADURA' : np.zeros((5, 255, 22))
    'PROG_LISTA'   : [1],
    'DISP_LISTA'   : [1],
    'ETIQUETA'     : [""]    
}

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('main/guiMain.ui', self)

        # SETEO GRAFICAS.
        self.graphWidget_1.setBackground('w')
        self.graphWidget_2.setBackground('w')
        self.graphWidget_3.setBackground('w')
        self.graphWidget_4.setBackground('w')

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
        self.caja_119.valueChanged.connect(self.valorCajas)
        self.caja_120.valueChanged.connect(self.valorCajas)
        self.caja_121.valueChanged.connect(self.valorCajas)
        self.caja_122.valueChanged.connect(self.valorCajas)

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

        # ACTUALIZO EXTREMOS CAJAS.
        self.caja_104.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_107.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_111.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_114.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_116.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_118.valueChanged.connect(self.seteoExtremoCajas)

        self.caja_202.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_203.valueChanged.connect(self.seteoExtremoCajas)

        self.caja_305.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_309.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_311.valueChanged.connect(self.seteoExtremoCajas)

        self.caja_402.valueChanged.connect(self.seteoExtremoCajas)

        self.caja_410.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_411.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_412.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_413.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_414.valueChanged.connect(self.seteoExtremoCajas)

        self.caja_420.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_421.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_422.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_423.valueChanged.connect(self.seteoExtremoCajas)
        self.caja_424.valueChanged.connect(self.seteoExtremoCajas)

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

        # EXPORTAR E IMPORTAR (desde excel).
        self.actionExportar.triggered.connect(self.exportar)

        # LISTA DE ERRORES.
        self.actionErrores.triggered.connect(lambda: window_6.show())

        # LLAMO A LOS GRAFICOS.
        self.plotSold()
        self.plotCalib()

    def PC_CS(self):
        """
        """        

        self.preguntoValorExtremoCajas()

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

            try:
                puerto.show()
                selecPort = window_3.seleccionarPuerto()
                puerto.confPuerto(selecPort, "OPEN")

                puerto.enviarDatosConfiguracion(cs)
                puerto.enviarDatosMonitor(cs, dispActual)

                for i in range(0, len(cs['DISP_LISTA'])):
                    dispActual = cs['DISP_LISTA'][i] - 1
                    progActual = cs['PROG_LISTA'][i] - 1     

                    if(window_3.combo_102.currentIndex() == 0):
                        puerto.enviarDatosServicios(cs, dispActual)  
                        puerto.enviarDatosSoldadura(cs, dispActual, progActual)

                    elif(window_3.combo_102.currentIndex() == 1):
                        puerto.enviarDatosServicios(cs, dispActual)  

                    else:
                        puerto.enviarDatosCalibracion(cs, dispActual)
                        puerto.enviarDatosServicios(cs, dispActual)                   
                        puerto.enviarDatosSoldadura(cs, dispActual, progActual)

                    # puerto.enviarDatosCalibracion(cs, dispActual)
                    # puerto.enviarDatosServicios(cs, dispActual)                   
                    # puerto.enviarDatosSoldadura(cs, dispActual, progActual)

                puerto.confPuerto(selecPort, "CLOSE")            
                puerto.hide()

            except:
                puerto.hide()
                mensaje = "El puerto [" + selecPort + "] no se reconoce."
                QMessageBox.warning(self, "Alerta", mensaje)

        elif pregunta == QMessageBox.Reset:
            #mando uno vacio.
            
            try:
                puerto.show()
                window_3.setearPuerto(puerto.seleccionoPuerto())
                selecPort = window_3.seleccionarPuerto()
                puerto.confPuerto(selecPort, "OPEN")

                puerto.bloquearProgramas()
                #puerto.borrarEeprom()

                puerto.confPuerto(selecPort, "CLOSE")            
                puerto.hide()

            except:
                puerto.hide()
                mensaje = "El puerto [" + selecPort + "] no se reconoce."
                QMessageBox.warning(self, "Alerta", mensaje)

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

            try:
                puerto.show()
                selecPort = window_3.seleccionarPuerto()
                puerto.confPuerto(selecPort, "OPEN")   

                cs['CONFIGURACION'] = puerto.recibirDatosConfiguracion(cs)
                cs['MONITOR'] = puerto.recibirDatosMonitor(cs, dispActual)
                
                for i in range(0, len(cs['DISP_LISTA'])):
                    dispActual = cs['DISP_LISTA'][i] - 1
                    progActual = cs['PROG_LISTA'][i] - 1   

                    if(window_3.combo_101.currentIndex() == 0):
                        
                        cs['CALIBRACION'] = puerto.recibirDatosCalibracion(cs, dispActual)
                        cs['SERVICIOS'] = puerto.recibirDatosServicios(cs, dispActual)                        
                    
                    else:

                        cs['CALIBRACION'] = puerto.recibirDatosCalibracion(cs, dispActual)
                        cs['SERVICIOS'] = puerto.recibirDatosServicios(cs, dispActual)
                        cs['SOLDADURA'] = puerto.recibirDatosSoldadura(cs, dispActual, progActual)

                    # cs['CALIBRACION'] = puerto.recibirDatosCalibracion(cs, dispActual)
                    # cs['SERVICIOS'] = puerto.recibirDatosServicios(cs, dispActual)
                    # cs['SOLDADURA'] = puerto.recibirDatosSoldadura(cs, dispActual, progActual)

                puerto.confPuerto(selecPort, "CLOSE")            
                puerto.hide()       

                window_3.cargoConfiguracion(cs)
                window_5.cargoTabla(cs)         

            except:
                puerto.hide()
                mensaje = "El puerto [" + selecPort + "] no se reconoce."
                QMessageBox.warning(self, "Alerta", mensaje)

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

            try:
                puerto.show()
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
            
            except:
                puerto.hide()
                mensaje = "El puerto [" + selecPort + "] no se reconoce."
                QMessageBox.warning(self, "Alerta", mensaje)

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

            try:
                puerto.show()
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
            
            except:
                puerto.hide()
                mensaje = "El puerto [" + selecPort + "] no se reconoce."
                QMessageBox.warning(self, "Alerta", mensaje)

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
        cs['CALIBRACION'], cs['SERVICIOS'] = window_4.copiarCalibServ(cs['CALIBRACION'], cs['SERVICIOS'])

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

        dato_1[disp][prog][19] = self.caja_121.value()  # Tolerancia 1.
        dato_1[disp][prog][20] = self.caja_122.value()  # Tolerancia 2.
        # dato_1[disp][prog][21] = comportamiento
        dato_1[disp][prog][22] = self.caja_119.value()  # Offset Intensidad.
        dato_1[disp][prog][23] = self.caja_120.value()  # Offset Fuerza.

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

        self.plotSold()
        self.plotCalib()

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
        self.caja_100.setValue( int( dato_1[disp][prog][0]) )
        self.caja_101.setValue( int( dato_1[disp][prog][1]) )
        self.caja_102.setValue( int( dato_1[disp][prog][2]) )
        self.caja_103.setValue( int( dato_1[disp][prog][3]) )
        self.caja_104.setValue(dato_1[disp][prog][4])           # float
        self.caja_105.setValue( int(dato_1[disp][prog][5]) )
        self.caja_106.setValue( int(dato_1[disp][prog][6]) )
        self.caja_107.setValue(dato_1[disp][prog][7])           # float
        self.caja_108.setValue( int(dato_1[disp][prog][8]) )
        self.caja_109.setValue( int(dato_1[disp][prog][9]) )
        self.caja_110.setValue( int(dato_1[disp][prog][10]) )
        self.caja_111.setValue(dato_1[disp][prog][11])          # float
        self.caja_112.setValue( int(dato_1[disp][prog][12]) )
        self.caja_113.setValue( int(dato_1[disp][prog][13]) )
        self.caja_114.setValue(dato_1[disp][prog][14])          # float
        self.caja_115.setValue( int(dato_1[disp][prog][15]) )
        self.caja_116.setValue(dato_1[disp][prog][16])          # float
        self.caja_117.setValue( int(dato_1[disp][prog][17]) )
        self.caja_118.setValue( int(dato_1[disp][prog][18]) )

        self.caja_119.setValue(dato_1[disp][prog][22])          # Offset intensidad. float
        self.caja_120.setValue( int(dato_1[disp][prog][23]) )   # Offset fuerza.
        self.caja_121.setValue( int(dato_1[disp][prog][19]) )   # Tolerancia 1.
        self.caja_122.setValue( int(dato_1[disp][prog][20]) )   # Tolerancia 2.

        #SERVICIOS
        self.caja_200.setValue( int(dato_2[disp][0][0]) )
        self.caja_201.setValue( int(dato_2[disp][0][1]) )
        self.caja_202.setValue( int(dato_2[disp][0][2]) )
        self.caja_203.setValue( int(dato_2[disp][0][3]) )
        self.caja_204.setValue( int(dato_2[disp][0][4]) )
        self.caja_205.setValue( int(dato_2[disp][0][5]) )
        self.caja_206.setValue( int(dato_2[disp][0][6]) )
        self.caja_207.setValue( int(dato_2[disp][0][7]) )
        self.caja_208.setValue( int(dato_2[disp][0][8]) )
        self.caja_209.setValue( int(dato_2[disp][0][9]) )
        self.caja_210.setValue( int(dato_2[disp][0][10]) )
        self.caja_211.setValue( int(dato_2[disp][0][11]) )

        #MONITOR
        self.caja_300.setValue( int(dato_3[0][0][0]) )
        self.caja_301.setValue( int(dato_3[0][0][1]) )
        self.caja_308.setValue( int(dato_3[0][0][2]) )
        self.caja_309.setValue(dato_3[0][0][3])                 # float
        self.caja_304.setValue( int(dato_3[0][0][4]) )
        self.caja_305.setValue( int(dato_3[0][0][5]) )

        #CALIBRACION
        self.caja_400.setValue( int(dato_4[disp][0][0]) )
        self.caja_401.setValue( int(dato_4[disp][0][1]) )
        self.caja_402.setValue( int(dato_4[disp][0][2]) )
        self.caja_403.setValue( int(dato_4[disp][0][3]) )
        self.caja_404.setValue( int(dato_4[disp][0][4]) )
        self.caja_405.setValue( int(dato_4[disp][0][5]) )       # % Fuerza 1
        self.caja_406.setValue( int(dato_4[disp][0][6]) )       # % Fuerza 2
        self.caja_407.setValue( int(dato_4[disp][0][7]) )       # % Fuerza 3
        self.caja_408.setValue( int(dato_4[disp][0][8]) )       # % Fuerza 4
        self.caja_409.setValue( int(dato_4[disp][0][9]) )       # % Fuerza 5
        self.caja_410.setValue( int(dato_4[disp][0][10]) )      # Valor Fuerza 1
        self.caja_411.setValue( int(dato_4[disp][0][11]) )      # Valor Fuerza 2
        self.caja_412.setValue( int(dato_4[disp][0][12]) )      # Valor Fuerza 3
        self.caja_413.setValue( int(dato_4[disp][0][13]) )      # Valor Fuerza 4
        self.caja_414.setValue( int(dato_4[disp][0][14]) )      # Valor Fuerza 5
        self.caja_415.setValue( int(dato_4[disp][0][15]) )      # % Intensidad 1
        self.caja_416.setValue( int(dato_4[disp][0][16]) )      # % Intensidad 2
        self.caja_417.setValue( int(dato_4[disp][0][17]) )      # % Intensidad 3
        self.caja_418.setValue( int(dato_4[disp][0][18]) )      # % Intensidad 4
        self.caja_419.setValue( int(dato_4[disp][0][19]) )      # % Intensidad 5
        self.caja_420.setValue(dato_4[disp][0][20])             # Valor Intensidad 1
        self.caja_421.setValue(dato_4[disp][0][21])             # Valor Intensidad 2
        self.caja_422.setValue(dato_4[disp][0][22])             # Valor Intensidad 3
        self.caja_423.setValue(dato_4[disp][0][23])             # Valor Intensidad 4
        self.caja_424.setValue(dato_4[disp][0][24])             # Valor Intensidad 5

        self.bloqueoSignals(False)
        self.ocultar()

    def seteoExtremoCajas(self):
        """
        Agrego los extremos de fuerza y corriente para las cajas.

        Fuerza Inferior: cs['CALIBRACION'][disp][0][10]
        Fuerza Superior: cs['CALIBRACION'][disp][0][14]

        Intensidad Inferior: cs['CALIBRACION'][disp][0][20] 
        Intensidad Superior: cs['CALIBRACION'][disp][0][19]   
        """

        self.bloqueoSignals(True) 

        disp = self.caja_1.value() - 1
        #prog = self.caja_2.value() - 1

        #FuerzaExtremoInferior = int(cs['CALIBRACION'][disp][0][10])
        FuerzaExtremoSuperior = int(cs['CALIBRACION'][disp][0][14])

        #IntensidadExtremoInferior = int(cs['CALIBRACION'][disp][0][20])     
        IntensidadExtremoSuperior = int(cs['CALIBRACION'][disp][0][24])       

        # --- EXTREMO SUPERIOR. 

        # SOLDADURA.
        self.caja_104.setMaximum(IntensidadExtremoSuperior)
        self.caja_107.setMaximum(IntensidadExtremoSuperior)
        self.caja_111.setMaximum(IntensidadExtremoSuperior)

        #self.caja_114.setMaximum(IntensidadExtremoSuperior)
        #self.caja_116.setMaximum(IntensidadExtremoSuperior)

        self.caja_114.setMaximum( self.caja_107.value() )
        self.caja_116.setMaximum( self.caja_107.value() )

        self.caja_118.setMaximum(FuerzaExtremoSuperior)

        # SERVICIOS.
        self.caja_202.setMaximum(FuerzaExtremoSuperior)
        self.caja_203.setMaximum(FuerzaExtremoSuperior)

        # MONITOR.
        self.caja_309.setMaximum(IntensidadExtremoSuperior)

        self.caja_305.setMaximum(FuerzaExtremoSuperior)
        self.caja_311.setMaximum(FuerzaExtremoSuperior)

        # CALIBRACION.
        self.caja_402.setMaximum(FuerzaExtremoSuperior)

        self.bloqueoSignals(False)

    def preguntoValorExtremoCajas(self):
        """
        """

        self.bloqueoSignals(True)

        disp = self.caja_1.value() - 1
        #prog = self.caja_2.value() - 1

        FuerzaExtremoInferior = int(cs['CALIBRACION'][disp][0][10])
        #FuerzaExtremoSuperior = int(cs['CALIBRACION'][disp][0][14])

        IntensidadExtremoInferior = int(cs['CALIBRACION'][disp][0][20])     
        #IntensidadExtremoSuperior = int(cs['CALIBRACION'][disp][0][24]) 

        # --- EXTREMO INFERIOR.
        
        caja = 0
        caja = self.caja_104
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_107
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_111
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_114
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_116
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_118
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        caja = 0
        caja = self.caja_202
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        caja = 0
        caja = self.caja_203
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        caja = 0
        caja = self.caja_309
        self.valorFueraDeRango(caja, IntensidadExtremoInferior)

        caja = 0
        caja = self.caja_305
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        caja = 0
        caja = self.caja_311
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        caja = 0
        caja = self.caja_402
        self.valorFueraDeRango(caja, FuerzaExtremoInferior)

        self.bloqueoSignals(False)

    def valorFueraDeRango(self, caja, extremoInferior):
        """
        """

        if((caja.value() < extremoInferior) and (caja.value() != 0)):
            self.cambioColor(caja, 'red')

            texto_1 = 'El valor [' + str(caja.value()) + '] esta por debajo del minimo.'
            texto_2 = 'Revise la calibracion.'
            texto = texto_1 + '\n' + texto_2
            QMessageBox.warning(
                self,
                'Error',
                texto
            )

            #caja.setValue(extremoInferior)
            self.cambioColor(caja, 'white') 

    def cambioColor(self, caja, color):
        """
        """

        #string = "color:" + color + ";"
        string = "background-color:" + color + ";"
        caja.setStyleSheet(string)

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

        dato_1[ : , : , 19] = self.caja_121.value() # Tolerancia 1.
        dato_1[ : , : , 20] = self.caja_122.value() # Tolerancia 2.
        dato_1[ : , : , 22] = self.caja_119.value() # Offset Intensidad.
        dato_1[ : , : , 23] = self.caja_120.value() # Offset Fuerza.

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
            
            for key in ['CONFIGURACION', 'MONITOR', 'CALIBRACION', 'SERVICIOS', 'SOLDADURA']:
                if( cs[key].shape == filename.item().get(key).shape ):
                    cs[key] = filename.item().get(key)
                else:
                    dimension = filename.item().get(key).shape
                    cs[key][ :dimension[0] , :dimension[1] , :dimension[2] ] = filename.item().get(key)[ : , : , :dimension[2] ]
                    
            cs['PROG_LISTA'] = filename.item().get("PROG_LISTA")
            cs['DISP_LISTA'] = filename.item().get("DISP_LISTA")
            cs['ETIQUETA'] = filename.item().get("ETIQUETA")
            
            window_3.cargoConfiguracion(cs)
            window_5.cargoTabla(cs)            
            self.seteoCajas()

        except:
            pass

    def exportar(self):
        """
        """

        os.chdir(os.path.expanduser("~"))

        fecha = str(datetime.datetime.now().date())
        nombre_archivo = ("save_" + fecha + ".xlsx") 

        direccion = QFileDialog.getSaveFileName(self, "Guardar", nombre_archivo)
        direccion = direccion[0]        
        
        # SOLDADURA.

        cols_sold = [
            'Programa',
            'Acercamiento',
            'Apriete',
            'Repeticion',
            'Soldadura 1',
            'Intensidad 1',
            'Frio 1',
            'Soldadura 2',
            'Intensidad 2',
            'Frio 2',
            'Impulsos',
            'Soldadura 3',
            'Intensidad 3',
            'Frio 3',
            'Soldadura 4',
            'Intensidad 4',
            'Soldadura 5',
            'Intensidad 5',
            'Forja',
            'Fuerza',
            'Tolerancia Sup.',
            'Tolerancia Inf.',
            'Comportamiento',
            'Offset I.',
            'Offset F.'
        ]

        cant_prog_disp = [0, 0, 0, 0, 0]
        for i in range( 0, len(cs['DISP_LISTA']) ):
            if cs['DISP_LISTA'][i] == 1:
                cant_prog_disp[0] += 1
            elif cs['DISP_LISTA'][i] == 2:
                cant_prog_disp[1] += 1
            elif cs['DISP_LISTA'][i] == 3:
                cant_prog_disp[2] += 1
            elif cs['DISP_LISTA'][i] == 4:
                cant_prog_disp[3] += 1
            elif cs['DISP_LISTA'][i] == 5:
                cant_prog_disp[4] += 1
            else:
                pass
         
        df_sold = [0, 0, 0, 0, 0]
        for disp in range(0, 5):
            aux = np.zeros( (cant_prog_disp[disp], 25) )
            for i in range(0, cant_prog_disp[disp]):
                prog = cs['PROG_LISTA'][i]
                aux[i][0] = prog
                aux[i][1:] = cs['SOLDADURA'][disp][prog]

            df_sold[disp] = pd.DataFrame(aux, columns=cols_sold)

        # SERVICIOS.

        cols_serv = [
            'Acercamiento',
            'Apriete',
            'Fuerza Fresado',
            'Fuerza Cambio E.',
            'Curva',
            'Incremento',
            'Puntos',
            'Alarma Puntos',
            'Contador Puntos',
            'Fresados',
            'Alarma Fresados',
            'Contador Fresados'
        ]

        df_serv = [0, 0, 0, 0, 0]
        for disp in range(0, 5):
            df_serv[disp] = pd.DataFrame(cs['SERVICIOS'][disp], columns=cols_serv)
            
        # CALIBRACION.        

        cols_calib = [
            'Acercamiento',
            'Apriete',
            'Fuerza',
            'Tiempo Soldadura',
            'Tiempo Mantenido',
            'Tension 1 [V]',
            'Tension 2 [V]',
            'Tension 3 [V]',
            'Tension 4 [V]',
            'Tension 5 [V]',
            'Fuerza 1 [daN]',
            'Fuerza 2 [daN]',
            'Fuerza 3 [daN]',
            'Fuerza 4 [daN]',
            'Fuerza 5 [daN]',
            'Porcentaje 1 [%]',
            'Porcentaje 2 [%]',
            'Porcentaje 3 [%]',
            'Porcentaje 4 [%]',
            'Porcentaje 5 [%]',
            'Intensidad 1 [KA]',
            'Intensidad 2 [KA]',
            'Intensidad 3 [KA]',
            'Intensidad 4 [KA]',
            'Intensidad 5 [KA]',
        ]

        df_calib = [0, 0, 0, 0, 0]
        for disp in range(0, 5):
            df_calib[disp] = pd.DataFrame(cs['CALIBRACION'][disp], columns=cols_calib)

        # GUARDAR.        

        start = [0, 0, 0, 0, 0]

        start[0] = 0
        start[1] = cant_prog_disp[0] + 3
        start[2] = cant_prog_disp[0] + cant_prog_disp[1] + 3 + 3
        start[3] = cant_prog_disp[0] + cant_prog_disp[1] + cant_prog_disp[2] + 3 + 3 + 3
        start[4] = cant_prog_disp[0] + cant_prog_disp[1] + cant_prog_disp[2] + cant_prog_disp[3] + 3 + 3 + 3 + 3

        # Los "+3" le dan la separacion en el archivo excel :)

        with pd.ExcelWriter(direccion, engine='xlsxwriter') as writer:

            for disp in range(0, 5):
                if disp + 1 in cs['DISP_LISTA']:
                    df_sold[disp].to_excel(writer, sheet_name='PROGRAMACION', index=False, startrow = start[disp])
                    df_serv[disp].to_excel(writer, sheet_name='SERVICIOS', index=False, startrow = start[disp])
                    df_calib[disp].to_excel(writer, sheet_name='CALIBRACION', index=False, startrow = start[disp])
                else:
                    pass

    def importar(self):
        """
        """

        pass

    def plotSold(self):
        """
        """

        disp = self.caja_1.value() - 1
        prog = self.caja_2.value() - 1

        #self.graphWidget_1.setXRange(0, 50)

        vectorX = [
            cs['SOLDADURA'][disp][prog][3],
            cs['SOLDADURA'][disp][prog][13],
            cs['SOLDADURA'][disp][prog][6],
            cs['SOLDADURA'][disp][prog][15],
            cs['SOLDADURA'][disp][prog][10]
        ]

        vectorY = [
            cs['SOLDADURA'][disp][prog][4],
            cs['SOLDADURA'][disp][prog][14],
            cs['SOLDADURA'][disp][prog][7],
            cs['SOLDADURA'][disp][prog][16],
            cs['SOLDADURA'][disp][prog][11]
        ]

        vectorTime = [
            cs['SOLDADURA'][disp][prog][5],
            cs['SOLDADURA'][disp][prog][8],
            cs['SOLDADURA'][disp][prog][12]
        ]
        
        ant = 0
        self.graphWidget_1.clear()
        for i in range( len(vectorX) ):
            
            x = vectorX[i]
            y = vectorY[i]
              
            if(vectorX[i] != 0):                  

                if(i==0):
                    # cuadrado inicial.
                    X = [0, 0, ant + x, ant + x]
                    Y = [0, y, y, 0]

                elif(i==1):
                    # rampa ascenso.    
                    ant += vectorTime[0]            
                    X = [ant, ant, ant + x, ant + x]    
                    Y = [0, y, vectorY[2], 0]

                elif(i==2):
                    # cuadrado intermedio.
                    if(vectorX[1]==0):
                        ant += vectorTime[0]
                    else:
                        pass

                    X = [ant, ant, ant + x, ant + x]
                    Y = [0, y, y, 0]

                elif(i==3):
                    # rampa descenso.
                    X = [ant, ant, ant + x, ant + x]
                    Y = [0, vectorY[2], y, 0]
                    
                else:      
                    # cuadrado final.
                    if(vectorX[3]==0):
                        ant += vectorTime[2]

                    ant += vectorTime[2]
                    X = [ant, ant, ant + x, ant + x]
                    Y = [0, y, y, 0]
                
            else:
                X = [0, 0, 0, 0]
                Y = [0, 0, 0, 0]            

            pen = pg.mkPen( color=(255, 0, 0), width=3 )
            self.graphWidget_1.plot(X, Y, pen=pen)

            ant += vectorX[i]

    def plotService(self):
        """
        """

        pass

    def plotCalib(self):
        """
        """

        disp = self.caja_1.value() - 1

        X1 = [
            cs['CALIBRACION'][disp][0][5],
            cs['CALIBRACION'][disp][0][6],
            cs['CALIBRACION'][disp][0][7],
            cs['CALIBRACION'][disp][0][8],
            cs['CALIBRACION'][disp][0][9]
        ]

        Y1 = [
            cs['CALIBRACION'][disp][0][10],
            cs['CALIBRACION'][disp][0][11],
            cs['CALIBRACION'][disp][0][12],
            cs['CALIBRACION'][disp][0][13],
            cs['CALIBRACION'][disp][0][14]
        ]

        X2 = [
            cs['CALIBRACION'][disp][0][15],
            cs['CALIBRACION'][disp][0][16],
            cs['CALIBRACION'][disp][0][17],
            cs['CALIBRACION'][disp][0][18],
            cs['CALIBRACION'][disp][0][19]
        ]

        Y2 = [
            cs['CALIBRACION'][disp][0][20],
            cs['CALIBRACION'][disp][0][21],
            cs['CALIBRACION'][disp][0][22],
            cs['CALIBRACION'][disp][0][23],
            cs['CALIBRACION'][disp][0][24]
        ]

        pen_1 = pg.mkPen( color=(0, 0, 255), width=3 )
        pen_2 = pg.mkPen( color=(255, 0, 0), width=3 )        

        # Fuerza.
        self.graphWidget_3.clear()

        self.graphWidget_3.setXRange(0, max(X1) )
        self.graphWidget_3.setYRange(0, max(Y1) )        
        
        self.graphWidget_3.plot(X1, Y1, pen=pen_1, symbol='o', symbolBrush=('b'))
        self.graphWidget_3.showGrid(x=True, y=True)

        # Corriente.
        self.graphWidget_4.clear()

        self.graphWidget_4.setXRange(0, max(X2) )
        self.graphWidget_4.setYRange(0, max(Y2) )
         
        self.graphWidget_4.plot(X2, Y2, pen=pen_2, symbol='o', symbolBrush=('r'))        
        self.graphWidget_4.showGrid(x=True, y=True)


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