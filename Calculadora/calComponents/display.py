
from calComponents.variables import LARGE_FONT,MINIMUN_WIDTH,TEXT_MARGEN
from calComponents.utils import isEmpty, isNumOrDot
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    numPressed = Signal(str)
    OperatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size : {LARGE_FONT}px')
        self.setMinimumHeight(LARGE_FONT * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGEN for side in range(4)])
        self.setMinimumWidth(MINIMUN_WIDTH)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Return, KEYS.Key_Enter]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
        isNumber = key in [KEYS.Key_0,KEYS.Key_1,KEYS.Key_2,KEYS.Key_3,KEYS.Key_4,KEYS.Key_5,KEYS.Key_6,KEYS.Key_7,KEYS.Key_8,KEYS.Key_9]

        if isEnter or text == '=':
            self.eqPressed.emit()
            return event.ignore()
        if isDelete or text == ('D'):
            self.delPressed.emit()
            return event.ignore()
        if isEsc or text == 'C':
            self.clearPressed.emit()
            return event.ignore()
        
        if isEmpty(text):
            return event.ignore()
        
        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.OperatorPressed.emit(text)
            return event.ignore()
        if isNumber:
            self.numPressed.emit(text)
            return event.ignore()

