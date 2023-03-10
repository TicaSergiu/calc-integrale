import time

from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QMessageBox
from sympy import Symbol, lambdify


class ValidatorFunctie(QValidator):
    def __init__(self, parent=None):
        super(ValidatorFunctie, self).__init__(parent)

    # verific daca functia este valida
    def validate(self, input_text, pos):
        if input_text == "":
            self.afiseaza_eroare("Functia nu poate fi sir vid")
            return QValidator.Invalid, input_text, pos
        if not input_text.__contains__("x"):
            self.afiseaza_eroare("Functia trebuie sa contina o variabila x")
            return QValidator.Invalid, input_text, pos
        try:
            lambdify(Symbol("x"), input_text)
        except Exception as e:
            if str(e).__contains__("'('"):
                self.afiseaza_eroare("O paranteza nu a fost inchisa")
                return QValidator.Invalid, input_text, pos
            if str(e).__contains__("')'"):
                self.afiseaza_eroare("O paranteza este in plus")
                return QValidator.Invalid, input_text, pos
            self.afiseaza_eroare("Functia nu este valida")
            print(e)
            return QValidator.Invalid, input_text, pos

        return QValidator.Acceptable, input_text, pos

    def afiseaza_eroare(self, mesaj):
        msg = QMessageBox(self.parent())
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mesaj)
        msg.setWindowTitle("Error")
        msg.exec_()
