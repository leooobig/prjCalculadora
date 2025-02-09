from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None , *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)

        #Título
        self.setWindowTitle('Calculadora')
        
        #Últimas coisas a serem feitas
    def adjustFixedSize(self):    
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    def makeBox(self):
        return QMessageBox(self)

