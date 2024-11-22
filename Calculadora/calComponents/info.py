from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from calComponents.variables import SMALL_FONT

class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text,parent)
        self.configStyle()
    
    def configStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setStyleSheet(f'font-size: {SMALL_FONT}px')
        
