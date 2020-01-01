from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic

import sys

import numpy as np

class Asistente(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('asistente/guiAsistente_1.ui', self)

        self.actualizoVenta1()
        self.actualizoVenta2()
        self.actualizoVenta3()

        self.caja_100.valueChanged.connect(self.actualizoVenta1)
        self.caja_101.valueChanged.connect(self.actualizoVenta1)
        self.caja_102.valueChanged.connect(self.actualizoVenta1)

        self.comboBox_100.currentIndexChanged.connect(self.actualizoVenta2)
        self.comboBox_101.currentIndexChanged.connect(self.actualizoVenta2)
        self.comboBox_102.currentIndexChanged.connect(self.actualizoVenta2)

        self.comboBox_200.currentIndexChanged.connect(self.actualizoVenta3)
        self.comboBox_201.currentIndexChanged.connect(self.actualizoVenta3)
        self.comboBox_202.currentIndexChanged.connect(self.actualizoVenta3)
        
    def actualizoVenta1(self):
        """
        """

        self.calculoReferencia()
        self.calculoDestructivo()

        self.calculoTiempo()
        self.calculoIntensidad()
        self.calculoFuerza()

    def actualizoVenta2(self):
        """
        """

        self.calculoDestructivo()

        self.calculoTiempo()
        self.calculoIntensidad()
        self.calculoFuerza()

    def actualizoVenta3(self):
        """
        """

        self.calculoDestructivo()

        self.calculoTiempo()
        self.calculoIntensidad()
        self.calculoFuerza()

    def calculoTiempo(self):
        """
        """

        #CHAPA/CHAPA
        if (self.caja_108.value() == 0):
            valor = 0
        elif (self.caja_108.value() <= 2):
            valor = (self.caja_108.value() * 10) + 5
        else:
            valor = (self.caja_108.value() * 20) - 12.5

        self.caja_103.setValue(valor)
        
        #CHAPA/TORNILLO
        if(self.comboBox_100.currentText() == "M4 / M5"):

            if(self.comboBox_102.currentText() == "0.7"):
                valor = 4
            elif(self.comboBox_102.currentText() == "0.8"):
                valor = 4
            elif(self.comboBox_102.currentText() == "1"):
                valor = 6
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M6 / M7"):

            if(self.comboBox_102.currentText() == "0.8"):
                valor = 6
            elif(self.comboBox_102.currentText() == "1"):
                valor = 7
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 7
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M8"):

            if(self.comboBox_102.currentText() == "1"):
                valor = 8
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 8
            elif(self.comboBox_102.currentText() == "1.6"):
                valor = 8
            elif(self.comboBox_102.currentText() == "2"):
                valor = 8
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 8
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M10"):

            if(self.comboBox_102.currentText() == "1.6"):
                valor = 8
            elif(self.comboBox_102.currentText() == "2"):
                valor = 8
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 9
            elif(self.comboBox_102.currentText() == "3.2"):
                valor = 10
            else:
                valor = 0

        if(valor == 0):
            self.caja_200.clear()

        else:
            self.caja_200.setValue(valor)

        #CHAPA/TUERCA
        if(self.comboBox_200.currentText() == "M4 / M5"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 2
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 2
            elif(self.comboBox_202.currentText() == "1"):
                valor = 2
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M6 / M7"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 3
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 3
            elif(self.comboBox_202.currentText() == "1"):
                valor = 3
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 3
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M8 / M9"):

            if(self.comboBox_202.currentText() == "0.8"):
                valor = 5
            elif(self.comboBox_202.currentText() == "1"):
                valor = 5
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 5
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 5
            elif(self.comboBox_202.currentText() == "2"):
                valor = 5
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 5
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M10"):

            if(self.comboBox_202.currentText() == "1"):
                valor = 6
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 6
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 6
            elif(self.comboBox_202.currentText() == "2"):
                valor = 6
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 6
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 6
            elif(self.comboBox_202.currentText() == "4"):
                valor = 6
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M12 / M14"):

            if(self.comboBox_202.currentText() == "1.6"):
                valor = 6
            elif(self.comboBox_202.currentText() == "2"):
                valor = 6
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 6
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 6
            elif(self.comboBox_202.currentText() == "4"):
                valor = 6
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M16"):

            if(self.comboBox_202.currentText() == "2"):
                valor = 8
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 8
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 8
            elif(self.comboBox_202.currentText() == "4"):
                valor = 8
            elif(self.comboBox_202.currentText() == "5"):
                valor = 8
            else:
                valor = 0

        if(valor == 0):
            self.caja_300.clear()

        else:
            self.caja_300.setValue(valor)

    def calculoIntensidad(self):
        """
        """

        #CHAPA/CHAPA
        if(self.caja_108.value() == 0):
            valor = 0
        elif(self.caja_108.value() <= 2):
            valor = (self.caja_108.value() * 1.13) + 7.1
        else:
            valor = (self.caja_108.value() * 1.5) + 5.8

        self.caja_104.setValue(valor)

        #CHAPA/TORNILLO
        if(self.comboBox_100.currentText() == "M4 / M5"):

            if(self.comboBox_102.currentText() == "0.7"):
                valor = 8.5
            elif(self.comboBox_102.currentText() == "0.8"):
                valor = 9
            elif(self.comboBox_102.currentText() == "1"):
                valor = 12
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M6 / M7"):

            if(self.comboBox_102.currentText() == "0.8"):
                valor = 14
            elif(self.comboBox_102.currentText() == "1"):
                valor = 16
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 22
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M8"):

            if(self.comboBox_102.currentText() == "1"):
                valor = 16
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 17
            elif(self.comboBox_102.currentText() == "1.6"):
                valor = 18
            elif(self.comboBox_102.currentText() == "2"):
                valor = 20
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 24
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M10"):

            if(self.comboBox_102.currentText() == "1.6"):
                valor = 21
            elif(self.comboBox_102.currentText() == "2"):
                valor = 24
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 26
            elif(self.comboBox_102.currentText() == "3.2"):
                valor = 29.2
            else:
                valor = 0

        if(valor == 0):
            self.caja_201.clear()
        else:
            if(self.comboBox_101.currentText() == "4"):
                self.caja_201.setValue(valor * 1.1)
            else:
                self.caja_201.setValue(valor)        

        #CHAPA/TUERCA
        if(self.comboBox_200.currentText() == "M4 / M5"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 13
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 14.7
            elif(self.comboBox_202.currentText() == "1"):
                valor = 15.5
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M6 / M7"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 12
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 12.7
            elif(self.comboBox_202.currentText() == "1"):
                valor = 13.4
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 14.2
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M8 / M9"):

            if(self.comboBox_202.currentText() == "0.8"):
                valor = 13.1
            elif(self.comboBox_202.currentText() == "1"):
                valor = 14.4
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 15.8
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 17
            elif(self.comboBox_202.currentText() == "2"):
                valor = 17.3
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 18.3
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M10"):

            if(self.comboBox_202.currentText() == "1"):
                valor = 15
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 16.3
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 17
            elif(self.comboBox_202.currentText() == "2"):
                valor = 17.5
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 19
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 20.5
            elif(self.comboBox_202.currentText() == "4"):
                valor = 22.5
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M12 / M14"):

            if(self.comboBox_202.currentText() == "1.6"):
                valor = 19
            elif(self.comboBox_202.currentText() == "2"):
                valor = 19.3
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 20
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 22.8
            elif(self.comboBox_202.currentText() == "4"):
                valor = 26.7
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M16"):

            if(self.comboBox_202.currentText() == "2"):
                valor = 19.6
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 20.5
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 23
            elif(self.comboBox_202.currentText() == "4"):
                valor = 27
            elif(self.comboBox_202.currentText() == "5"):
                valor = 31
            else:
                valor = 0

        if(valor == 0):
            self.caja_301.clear()

        else:
            if(self.comboBox_201.currentText() == "4"):
                self.caja_301.setValue(valor * 1.1)
            else:
                self.caja_301.setValue(valor)            

    def calculoFuerza(self):
        """
        """

        #CHAPA/CHAPA
        if(self.caja_108.value() == 0):
            valor = 0
        elif(self.caja_108.value() <= 2):
            valor = (self.caja_108.value() * 1.64) + 0.45
        else:
            valor = (self.caja_108.value() * 1.30) + 0.7

        self.caja_105.setValue(valor)

        #CHAPA/TORNILLO
        if(self.comboBox_100.currentText() == "M4 / M5"):

            if(self.comboBox_102.currentText() == "0.7"):
                valor = 2.6
            elif(self.comboBox_102.currentText() == "0.8"):
                valor = 2.8
            elif(self.comboBox_102.currentText() == "1"):
                valor = 3.5
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M6 / M7"):

            if(self.comboBox_102.currentText() == "0.8"):
                valor = 3.5
            elif(self.comboBox_102.currentText() == "1"):
                valor = 4.5
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 5
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M8"):

            if(self.comboBox_102.currentText() == "1"):
                valor = 6
            elif(self.comboBox_102.currentText() == "1.25"):
                valor = 6.5
            elif(self.comboBox_102.currentText() == "1.6"):
                valor = 7
            elif(self.comboBox_102.currentText() == "2"):
                valor = 8
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 9.5
            else:
                valor = 0

        elif(self.comboBox_100.currentText() == "M10"):

            if(self.comboBox_102.currentText() == "1.6"):
                valor = 8.5
            elif(self.comboBox_102.currentText() == "2"):
                valor = 9
            elif(self.comboBox_102.currentText() == "2.4"):
                valor = 9.5
            elif(self.comboBox_102.currentText() == "3.2"):
                valor = 12.5
            else:
                valor = 0

        if(valor == 0):
            self.caja_202.clear()

        else:
            if(self.comboBox_101.currentText() == "4"):
                self.caja_202.setValue(valor * 1.1)
            else:
                self.caja_202.setValue(valor)                

        #CHAPA/TUERCA
        if(self.comboBox_200.currentText() == "M4 / M5"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 3
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 3.5
            elif(self.comboBox_202.currentText() == "1"):
                valor = 4
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M6 / M7"):

            if(self.comboBox_202.currentText() == "0.7"):
                valor = 3.5
            elif(self.comboBox_202.currentText() == "0.8"):
                valor = 4.6
            elif(self.comboBox_202.currentText() == "1"):
                valor = 5.7
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 7
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M8 / M9"):

            if(self.comboBox_202.currentText() == "0.8"):
                valor = 5.7
            elif(self.comboBox_202.currentText() == "1"):
                valor = 6.3
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 7
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 7.5
            elif(self.comboBox_202.currentText() == "2"):
                valor = 8.5
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 10
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M10"):

            if(self.comboBox_202.currentText() == "1"):
                valor = 7
            elif(self.comboBox_202.currentText() == "1.25"):
                valor = 7.5
            elif(self.comboBox_202.currentText() == "1.6"):
                valor = 8
            elif(self.comboBox_202.currentText() == "2"):
                valor = 9.2
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 10
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 11
            elif(self.comboBox_202.currentText() == "4"):
                valor = 11.5
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M12 / M14"):

            if(self.comboBox_202.currentText() == "1.6"):
                valor = 8.8
            elif(self.comboBox_202.currentText() == "2"):
                valor = 9.2
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 10
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 12.5
            elif(self.comboBox_202.currentText() == "4"):
                valor = 16
            else:
                valor = 0

        elif(self.comboBox_200.currentText() == "M16"):

            if(self.comboBox_202.currentText() == "2"):
                valor = 9.8
            elif(self.comboBox_202.currentText() == "2.4"):
                valor = 10
            elif(self.comboBox_202.currentText() == "3.2"):
                valor = 12.5
            elif(self.comboBox_202.currentText() == "4"):
                valor = 16
            elif(self.comboBox_202.currentText() == "5"):
                valor = 17.2
            else:
                valor = 0

        if(valor == 0):
            self.caja_302.clear()

        else:
            if(self.comboBox_201.currentText() == "4"):
                self.caja_302.setValue(valor * 1.1)
            else:
                self.caja_302.setValue(valor)                

    def calculoReferencia(self):
        """
        """

        #ELECTRODO
        valor = np.array([self.caja_100.value(), self.caja_101.value(), self.caja_102.value()])
        valor = (2*np.amax(valor)) + 3
        self.caja_106.setValue(valor)

        #TOTAL
        self.caja_107.setValue(self.caja_100.value() + self.caja_101.value() + self.caja_102.value())

        #REFERENCIA
        if self.caja_102.value() == 0:
            valor = np.array([self.caja_100.value(), self.caja_101.value()])
        else:
            valor = np.array([self.caja_100.value(), self.caja_101.value(), self.caja_102.value()])

        valor = np.mean(valor)
        self.caja_108.setValue(valor)

    def calculoDestructivo(self):
        """
        """

        valor_1 = 5*(min(self.caja_100.value(), self.caja_101.value())**0.5)
        valor_2 = 5*(min(self.caja_101.value(), self.caja_102.value())**0.5)
        valor_3 = int(self.comboBox_101.currentText()) * 1.1
        valor_4 = int(self.comboBox_201.currentText()) * 1.1

        self.caja_109.setValue(valor_1)
        self.caja_110.setValue(valor_2)
        self.caja_203.setValue(valor_3)
        self.caja_303.setValue(valor_4)

    def datosAsistente(self):
        """
        """
        
        programa = self.caja_1.value()

        if(self.tabWidget.currentIndex() == 0):
            valor_1 = self.caja_103.value()
            valor_2 = self.caja_104.value()
            valor_3 = self.caja_105.value()

            return programa, valor_1, valor_2, valor_3

        elif (self.tabWidget.currentIndex() == 1):
            valor_1 = self.caja_200.value()
            valor_2 = self.caja_201.value()
            valor_3 = self.caja_202.value()

            return programa, valor_1, valor_2, valor_3

        else:
            valor_1 = self.caja_300.value()
            valor_2 = self.caja_301.value()
            valor_3 = self.caja_302.value()

            return programa, valor_1, valor_2, valor_3

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = Asistente()
    window.show()

    sys.exit(app.exec_())