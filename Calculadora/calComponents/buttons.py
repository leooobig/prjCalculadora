import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from calComponents.variables import MEDIUM_FONT
from calComponents.utils import isValidNumber, isEmpty, isPoint, convertNumber

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Calculadora.calComponents.display import Display
    from Calculadora.calComponents.main_window import MainWindow
    from Calculadora.calComponents.info import Info

class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT)
        self.setFont(font)
        self.setMinimumSize(75,75)


class ButtonGrid(QGridLayout):
    def __init__(self, display:'Display',info: 'Info', window:'MainWindow', *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        
        self.window = window
        self.display = display
        self.info = info
        self._left : str | float | None = None
        self._right : float | None = None
        self._op = None
        self._equation = ''
        self._equationInitialValue = 'Sua Conta'
        self._makeGrid()

        self.equation = self._equationInitialValue

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,value):
        self._equation = value
        self.info.setText(value)

    def testeConection(self, *args):
        print(f'tecla= {args}')

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.numPressed.connect(self._insertTextToDisplay)
        self.display.OperatorPressed.connect(self._configLeftOp)
        
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isValidNumber(button.text()) | isEmpty(button.text()) | isPoint(button.text()): #Botões especiais
                    button.setStyleSheet('background-color:#16658a')
                    button.setProperty('cssClass:', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertTextToDisplay, buttonText)
                self._connectButtonClicked(button,slot)
    
    def _makeSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args,**kwargs)
        return realSlot
    
    def _makeEquation(self, numLeft:float|str, op:str|None, numRight:float|None = None):
        if numRight is None:
            return f'{numLeft} {op}'
        return f'{numLeft} {op} {numRight}'
    
    @Slot()
    def _insertTextToDisplay(self, text):
        newTextDisplay = self.display.text() + text
        if not isValidNumber(newTextDisplay):
            return
        self.display.insert(text)
        self.display.setFocus()

    def _connectButtonClicked(self, button:Button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self,button):
        text = button.text()
        
        if text == 'C':
            self._connectButtonClicked(button,self._clear)
        
        if text in '+-*/^':
            slot = self._makeSlot(self._configLeftOp,text)
            self._connectButtonClicked(button, slot)

        if text == '=':
            self._connectButtonClicked(button, self._eq)
       
        if text == 'N':
            self._connectButtonClicked(button, self._conversionNumber)
        
        if text == 'D':
            self._connectButtonClicked(button,self._backspace)

    @Slot()
    def _clear(self):
        self.equation = self._equationInitialValue
        self._left = None
        self._right = None
        self.display.clear()
        self.display.setFocus()
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self,text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()
        
        if not isValidNumber(displayText) and self._left == None:
            self._showError('Você não digitou nada')
            return
        
        if self._left is None:
            self._left = convertNumber(displayText)

        self._op = text
        self.equation = self._makeEquation(self._left, self._op)

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()
        if not isValidNumber(displayText):
            self._showError('Conta incompleta')
            return
        
        if self._left is not None:
            self._right = convertNumber(displayText)
            self.equation = self._makeEquation(self._left, self._op, self._right)
            result = 'error'

            try:
                if '^' in self.equation and isinstance(self._left, int | float):
                    result = math.pow(self._left, self._right)
                else:
                    result = eval(self.equation)
            except ZeroDivisionError:
                self._showError('Número não pode ser dividido por zero')
            except OverflowError:
                self._showError('O resultado esta fora dos limites permitidos da calculadora')

            self.info.setText(f'{self.equation} = {result}')
            self._left  = result
            self._right = None

            if self._left == 'error':
                self._left = None
        else:
            self._showError('Conta incompleta')
    
    @Slot()
    def _conversionNumber(self):
        displayText = self.display.text()
        self.display.clear()
        
        newNumber = convertNumber(displayText) * -1
        
        self.display.setText(str(newNumber))
        self.display.setFocus()

    
    def _showError(self, text):
        msgBox = self.window.makeBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
 