from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QComboBox, QSpinBox, QLineEdit, QMessageBox, QPushButton
from PyQt5 import uic, QtGui, QtCore

import sys

#import numpy as np

#class Tabla(QDialog):
class Tabla(QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('tabla/guiTabla.ui', self)

        self.seteoCeldas(0, 1)
        self.btn_100.clicked.connect(self.agregarFilas)
        self.btn_101.clicked.connect(self.quitarFilas)

        #self.btn_102.clicked.connect(self.juntoFilas)

        # Timer.

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.juntoFilas)

        self.timer.start()

        # Grilla.

        self.createMap()

    def quitarFilas(self):
        """
        """

        fila = self.table_100.currentRow()        

        if(fila == -1):
            fila = 0
        else:
            fila = fila

        if(self.table_100.rowCount() > 1):

            programa = self.table_100.cellWidget(fila, 0).value()
            #dispositivo = int(self.table_100.cellWidget(fila, 1).currentText())

            texto = '¿Quiere borrar el programa [' + str(programa) + '] - fila [' + str(fila+1) + '] de la Tabla?'
            pregunta = QMessageBox.question(
                self, 
                "Atencion", 
                texto, 
                #QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                QMessageBox.Yes | QMessageBox.Cancel
            )

            if pregunta == QMessageBox.Yes:
                #bloquearPrograma(programa, dispositivo)
                self.table_100.removeRow(fila) 

            else:
                pass
            
        #cantidad = int(self.combo_100.currentText())
        #for i in range(0, cantidad):
        #    self.table_100.removeRow(1)        

    def agregarFilas(self):
        """
        """

        #maxRowsInsert = int(self.combo_100.currentText())
        maxRowsInsert = int(self.caja_100.value())
        rowCount = self.table_100.rowCount() - 1
        for i in range(0, maxRowsInsert):
            if( rowCount < 255 ):
                number = rowCount + i + 1
                self.table_100.insertRow(number)
                self.seteoCeldas(number, 1)

    def seteoCeldas(self, fila, programa):
        """
        """
        
        opciones_combobox = ["1", "2", "3", "4", "5"]
        combo_1 = QComboBox()
        combo_1.addItems(opciones_combobox)

        item_1 = QSpinBox()
        item_1.setRange(1, 255)
        item_1.setValue(programa)

        texto_1 = QLineEdit()

        # Recordar que cuando se activa "inicio", se cambia el item por "fin" y a los
        # items de por medio se los cambio por "continuar"
        
        opciones_combobox = ["Individual", "Inicio", "Continuar", "Fin"]
        #opciones_combobox = ["Individual", "Inicio", "Fin"]
        #opciones_combobox = ["Individual", "Inicio"]
        combo_2 = QComboBox()
        combo_2.addItems(opciones_combobox)

        self.table_100.setCellWidget(fila, 0, item_1)
        self.table_100.setCellWidget(fila, 1, combo_1)
        self.table_100.setCellWidget(fila, 2, combo_2)
        self.table_100.setCellWidget(fila, 3, texto_1)

    def seteoFila(self, fila, prog, disp, funcion, etiqueta):
        """
        """

        Programa = self.table_100.cellWidget(fila, 0)
        Dispositivo = self.table_100.cellWidget(fila, 1)
        Funcion = self.table_100.cellWidget(fila, 2)
        Etiqueta = self.table_100.cellWidget(fila, 3)

        Programa.setValue(prog)
        Dispositivo.setCurrentText(str(disp))

        if funcion == 10:
            Funcion.setCurrentText("Individual")
        elif funcion == 20:
            Funcion.setCurrentText("Inicio")
        elif funcion == 30:
            Funcion.setCurrentText("Fin")
        else:
            Funcion.setCurrentText("Continuar")
            
        Etiqueta.setText(etiqueta)

    def datosTabla(self):
        """
        Valor Funcion retorna 10, 20, 30, 40, 50

        10: programa individual
        20: inicio
        30: fin
        40: continuar
        50: programa bloqueado
        """

        self.juntoFilas()

        vectorProgramas = []
        vectorDispositivo = []
        vectorFuncion = []
        vectorEtiqueta = []

        filas_max = self.table_100.rowCount()
        for i in range(0, filas_max):
            Programa = self.table_100.cellWidget(i, 0)
            Dispositivo = self.table_100.cellWidget(i, 1)
            Funcion = self.table_100.cellWidget(i, 2)
            Etiqueta = self.table_100.cellWidget(i, 3)

            vectorProgramas.append(Programa.value())
            vectorDispositivo.append(int(Dispositivo.currentText()))
            vectorFuncion.append(Funcion.currentText())
            vectorEtiqueta.append(Etiqueta.text())

        for i in range(0, filas_max):

            if(vectorFuncion[i] == "Individual"):
                valorFuncion = 10

            elif (vectorFuncion[i] == "Inicio"):
                valorFuncion = 20

            elif (vectorFuncion[i] == "Fin"):
                valorFuncion = 30

            elif(vectorFuncion[i] == "Continuar"):
                valorFuncion = 40

            else:
                valorFuncion = 10

            vectorFuncion[i] = valorFuncion

        return vectorProgramas, vectorDispositivo, vectorFuncion, vectorEtiqueta

    def cargoTabla(self, cs):
        """
        """

        vectorProgramas = cs['PROG_LISTA']
        vectorDispositivo = cs['DISP_LISTA']
        #vectorFuncion = cs['SOLDADURA']
        vectorEtiqueta = cs['ETIQUETA']

        filas_max = self.table_100.rowCount()
        for i in range(0, filas_max):
            self.table_100.removeRow(1)

        filas_max = len(vectorDispositivo) - 1
        for i in range(0, filas_max):
            self.agregarFilas()

        filas_max = len(vectorDispositivo) 
        for i in range(0, filas_max):
            disp = vectorDispositivo[i] - 1
            prog = vectorProgramas[i] - 1
            
            self.seteoFila(i, vectorProgramas[i], vectorDispositivo[i], cs['SOLDADURA'][disp][prog][21], vectorEtiqueta[i])

        self.juntoFilas()

    def juntoFilas(self):
        """
        """
        
        bandera_1 = False
        filas_max = self.table_100.rowCount()
        function = [ self.table_100.cellWidget(i, 2) for i in range(0, filas_max) ]

        countFin = 0
        countInicio = 0
        for i in range(0, filas_max):
            if( function[i].currentText() == 'Inicio' ):
                countInicio += 1
            elif( function[i].currentText() == 'Fin' ):
                countFin += 1
            else:
                pass

        for i in range(0, filas_max):
            if( function[i].currentText() == 'Inicio' ):
                bandera_1 = True

            elif( function[i].currentText() == 'Fin' ):
                bandera_1 = False

            else:
                if(bandera_1 == True):
                    function[i].setEnabled(False)
                    function[i].setCurrentIndex(2)
                else:
                    function[i].setEnabled(True)
                    function[i].setCurrentIndex(0)

    def createMap(self):
        """
        """

        btn = [ QPushButton( str(i+1) ) for i in range(0, 256) ]

        prog = 0
        for i in range(0, 16):
            for j in range(0, 16):
                
                btn[prog].setFixedSize( QtCore.QSize(25, 25) )
                self.gridLayout.addWidget( btn[prog], i, j )

                if(prog != 0):
                    btn[prog].setDisabled(True)

                prog += 1

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = Tabla()
    window.show()

    sys.exit(app.exec_())