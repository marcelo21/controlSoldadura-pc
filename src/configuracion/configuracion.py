from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic

import sys

class Configuracion(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('configuracion/guiConfiguracion.ui', self)

        #self.buttonBox.accepted.connect(self.datosConfiguracion)

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
            pulsador = True
        else:
            pulsador = False

        if self.r_btn_104.isChecked():
            soldadura = 10
        else:
            soldadura = 30

        if self.r_btn_106.isChecked():
            regulacion = True
        else:
            regulacion = False

        valor_0  = pulsador
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


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = Configuracion()
    window.show()

    sys.exit(app.exec_())