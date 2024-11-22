import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from Calculadora.calComponents.main_window import MainWindow
from Calculadora.calComponents.variables import WINDOW_IMG_ICON
from Calculadora.calComponents.display import Display 
from Calculadora.calComponents.info import Info
from Calculadora.calComponents.style import setupTheme
from Calculadora.calComponents.buttons import ButtonGrid


if '__main__' == __name__:

    #Cria Aplicação
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    #Defini ícone
    icon = QIcon(str(WINDOW_IMG_ICON))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #Info
    info = Info('Qualquer Coisa')
    window.addWidgetToVLayout(info) 

    #Display
    display = Display()
    window.addWidgetToVLayout(display)

    #Grid
    buttonsGrid = ButtonGrid(display,info,window)
    window.vLayout.addLayout(buttonsGrid)
   
    
    window.adjustFixedSize()

    window.show()
    app.exec()
