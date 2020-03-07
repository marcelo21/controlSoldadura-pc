from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic

import sys

import numpy as np

import re

class Copiar(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('copiar/guiCopiar.ui', self)

        self.cadena = ""
        self.auxiliar = ""

        self.t_caja_100.textChanged.connect(self.filtroCaracteres)

    def filtroCaracteres(self):
        """
        """

        self.cadena = self.t_caja_100.text()
        self.auxiliar = str(re.sub('[^0123456789,-]', '', self.cadena))
        self.t_caja_100.setText(self.auxiliar)

    def identifico(self, x):
        """
        """

        bandera_1 = False

        cadena_1 = ""
        cadena_2 = ""

        aux_1 = 0
        
        largo = len(self.auxiliar)

        ORIGEN = self.caja_100.value() - 1
        DISP_INI = int(self.combo_100.currentText()) - 1
        DISP_FIN = int(self.combo_101.currentText()) - 1

        self.auxiliar = self.t_caja_100.text()
        
        if( (',' in self.auxiliar) or ('-' in self.auxiliar) ): 

            #analizo todo el vector.
            for i in self.auxiliar:
                aux_1 += 1

                if(i == '-'):                    
                    # Para atras.
                    inicio = int(cadena_1) - 1

                    # Para adelante.    
                    cadena_2 = ""
                    for j in self.auxiliar[aux_1:]:
                        if(j == ','):
                            break
                        else:
                            cadena_2 = cadena_2 + j

                    fin = int(cadena_2)                     

                    x[DISP_FIN, inicio:fin, :] = x[DISP_INI, ORIGEN, :]

                    bandera_1 = True
                    cadena_1 = ""
                    cadena_2 = ""
                    pass

                elif(i == ','):
                    # Copio la parte de atras.
                    if(bandera_1 == False):
                        DESTINO = int(cadena_1) - 1
                        x[DISP_FIN, DESTINO, :] = x[DISP_INI, ORIGEN, :]

                        bandera_1 = False
                        cadena_1 = ""

                    # Copio la parte de adelante.
                    else:
                        cadena_2 = ""
                        for j in self.auxiliar[aux_1:]:
                            if(j == ','):
                                break
                            else:
                                cadena_2 = cadena_2 + j

                        DESTINO = int(cadena_2) - 1
                        x[DISP_FIN, DESTINO, :] = x[DISP_INI, ORIGEN, :]

                        #bandera_1 = False
                        cadena_1 = ""
                        cadena_2 = ""

                else:
                    cadena_1 = cadena_1 + i

            #analizo solo la ultima parte (es muy importante).
            if(self.auxiliar[largo - 1] != ',' or self.auxiliar[largo - 1] != '-'):
                DESTINO = int(cadena_1) - 1
                x[DISP_FIN, DESTINO, :] = x[DISP_INI, ORIGEN, :]

        else:
            DESTINO = int(self.auxiliar) - 1
            x[DISP_FIN, DESTINO, :] = x[DISP_INI, ORIGEN, :]

        return x
    
    def copiarCalibServ(self, x, y):
        """
        """

        DISP_INI = int(self.combo_100.currentText()) - 1
        DISP_FIN = int(self.combo_101.currentText()) - 1

        # Calibracion.
        if(self.checkBox_1.isChecked()):
            
            x[DISP_FIN, :, :] = x[DISP_INI, :, :]

        # Servicios.
        if(self.checkBox_2.isChecked()):
            
            y[DISP_FIN, :, :] = y[DISP_INI, :, :]

        return x, y


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = Copiar()
    window.show()

    sys.exit(app.exec_())