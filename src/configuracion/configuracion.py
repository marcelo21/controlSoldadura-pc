from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic

import sys

class Configuracion(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('configuracion/guiConfiguracion.ui', self)

    def setearPuerto(self, puertos):
        """
        """

        largo = len(puertos)
        for i in range (0, largo):
            index = self.combo_100.findText(puertos[i])    
            self.combo_100.setCurrentIndex(index) 

    def seleccionarPuerto(self):
        """
        """

        return self.combo_100.currentText() 

    def datosConfiguracion(self):
        """
        """

        finCiclo =  self.caja_100.value()        

        if self.r_btn_100.isChecked():
            incremento = True
        else:
            incremento = False

        if self.r_btn_102.isChecked():
            medicion = True
        else:
            medicion = False

        if self.r_btn_104.isChecked():
            soldadura = 10
        else:
            soldadura = 30

        if self.r_btn_106.isChecked():
            regulacion = True
        else:
            regulacion = False

        valor_0  = medicion
        valor_1  = regulacion
        valor_2  = 0
        valor_3  = 0
        valor_4  = 0
        valor_5  = 0
        valor_6  = 0
        valor_7  = 0
        valor_8  = 0
        valor_9  = 0
        valor_10 = 0
        valor_11 = 0
        valor_12 = 0
        valor_13 = 0
        valor_14 = 0
        valor_15 = 0

        configuracionesVarias = (valor_15 << 15) | (valor_14 << 14) | (valor_13 << 13) | (valor_12 << 12) | (valor_11 << 11) | (valor_10 << 10) | (valor_9 << 9) | (valor_8 << 8) | (valor_7 << 7) | (valor_6 << 6) | (valor_5 << 5) | (valor_4 << 4) | (valor_3 << 3) | (valor_2 << 2) | (valor_1 << 1) | (valor_0 << 0)

        # Para volver a tener un solo bit hacemos ( valor_n >> n ) & 1
        # Ejemplo: ( valor_11 >> 11 ) & 1

        return soldadura, incremento, finCiclo, configuracionesVarias

    def cargoConfiguracion(self, cs):
        """
        """

        soldadura = int(cs['CONFIGURACION'][0][0][0])
        incremento = int(cs['CONFIGURACION'][0][0][1])
        finCiclo = int(cs['CONFIGURACION'][0][0][2])
        valor = int(cs['CONFIGURACION'][0][0][3])

        valor_0  = (valor >> 0)  & 1 # Medicion
        valor_1  = (valor >> 1)  & 1 # Regulacion
        valor_2  = (valor >> 2)  & 1 # 
        valor_3  = (valor >> 3)  & 1 # 
        valor_4  = (valor >> 4)  & 1 # 
        valor_5  = (valor >> 5)  & 1 # 
        valor_6  = (valor >> 6)  & 1 # 
        valor_7  = (valor >> 7)  & 1 # 
        valor_8  = (valor >> 8)  & 1 # 
        valor_9  = (valor >> 9)  & 1 # 
        valor_10 = (valor >> 10) & 1 # 
        valor_11 = (valor >> 11) & 1 # 
        valor_12 = (valor >> 12) & 1 # 
        valor_13 = (valor >> 13) & 1 # 
        valor_14 = (valor >> 14) & 1 # 
        valor_15 = (valor >> 15) & 1 #
        
        self.caja_100.setValue(finCiclo)

        if incremento == 1:
            self.r_btn_100.setChecked(True)
            self.r_btn_101.setChecked(False)
        else:
            self.r_btn_100.setChecked(False)
            self.r_btn_101.setChecked(True)

        if soldadura == 10:
            self.r_btn_104.setChecked(True)
            self.r_btn_105.setChecked(False)
        else:
            self.r_btn_104.setChecked(False)
            self.r_btn_105.setChecked(True)

        if valor_0 == True:
            self.r_btn_102.setChecked(True)
            self.r_btn_103.setChecked(False)
        else:
            self.r_btn_102.setChecked(False)
            self.r_btn_103.setChecked(True)

        if valor_1 == True:
            self.r_btn_106.setChecked(True)
            self.r_btn_107.setChecked(False)
        else:
            self.r_btn_106.setChecked(False)
            self.r_btn_107.setChecked(True)


class ListaErrores(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi('configuracion/guiTablaErrores.ui', self)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window_1 = Configuracion()
    window_2 = ListaErrores()

    window_1.show()

    sys.exit(app.exec_())