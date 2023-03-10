import random
import sys
import timeit

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.integrate import quadrature
from scipy.interpolate import lagrange

from metode import *
from validatori import *


# fereastra metode integrare

class Fereastra(QDialog):
    def __init__(self, parent=None):
        super(Fereastra, self).__init__(parent)
        self.setWindowTitle('Integrare numerica')

        self.a = None
        self.b = None
        self.f = None
        self.limita = None
        self.iter_curenta = None
        self.timer = None
        self.validator_functie = ValidatorFunctie(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.label_functie = QLabel('Introduceti o functie: ')
        self.functie = QLineEdit()

        self.label_start_interval = QLabel('a: ')
        self.start_interval = QLineEdit()

        self.label_sfarsit_interval = QLabel('b: ')
        self.sfarsit_interval = QLineEdit()

        self.label_iteratii = QLabel('Numar iteratii/Eroare: ')
        self.nr_iteratii = QLineEdit()

        self.label_met_composita = QLabel('Metoda composita? ')

        self.btn_met_dreptunghiului = QRadioButton('Metoda dreptunghiului')
        self.btn_met_trapez = QRadioButton('Metoda trapez')
        self.btn_met_simpson = QRadioButton('Metoda Simpson')
        self.check_trapez_compozit = QCheckBox()
        self.check_simpson_compozit = QCheckBox()

        self.btn_calculeaza = QPushButton("Calculeaza")
        self.btn_calculeaza.clicked.connect(self.calculeaza)

        self.fisier = QPushButton("Incarca din fisier")
        self.fisier.clicked.connect(self.citeste_fisier)

        self.label_timp = QLabel('Timp executie:')
        self.timp_executie = QLineEdit()
        self.timp_executie.setEnabled(False)

        self.label_aprox = QLabel('Valoare aproximata:')
        self.val_aprox = QLineEdit()
        self.val_aprox.setEnabled(False)

        self.label_exacta = QLabel('Valoare exacta:')
        self.val_exacta = QLineEdit()
        self.val_exacta.setEnabled(False)

        self.animatie = QPushButton("Sari peste animatie")
        self.animatie.clicked.connect(self.stop_animatie)

        self.lista = [self.timp_executie, self.label_timp, self.val_aprox, self.label_aprox, self.val_exacta,
                      self.label_exacta, self.label_aprox, self.animatie]

        for i in self.lista:
            i.hide()

        layout = QGridLayout()
        layout.addWidget(self.label_functie, 0, 0)
        layout.addWidget(self.functie, 0, 1)
        layout.addWidget(self.label_start_interval, 1, 0)
        layout.addWidget(self.start_interval, 1, 1)
        layout.addWidget(self.label_sfarsit_interval, 2, 0)
        layout.addWidget(self.sfarsit_interval, 2, 1)
        layout.addWidget(self.label_iteratii, 3, 0)
        layout.addWidget(self.nr_iteratii, 3, 1)
        layout.addWidget(self.canvas, 0, 2, 10, 1)
        layout.addWidget(self.btn_met_dreptunghiului, 4, 0)
        layout.addWidget(self.label_met_composita, 4, 1, 1, 2)
        layout.addWidget(self.btn_met_trapez, 5, 0)
        layout.addWidget(self.check_trapez_compozit, 5, 1)
        layout.addWidget(self.btn_met_simpson, 6, 0)
        layout.addWidget(self.check_simpson_compozit, 6, 1)
        layout.addWidget(self.fisier, 7, 0)
        layout.addWidget(self.btn_calculeaza, 9, 0)
        layout.addWidget(self.timp_executie, 5, 4)
        layout.addWidget(self.label_timp, 5, 3)
        layout.addWidget(self.val_aprox, 6, 4)
        layout.addWidget(self.label_aprox, 6, 3)
        layout.addWidget(self.val_exacta, 7, 4)
        layout.addWidget(self.label_exacta, 7, 3, 1, 2)
        layout.addWidget(self.animatie, 4, 3, 1, 2)

        self.setLayout(layout)

    def calculeaza(self):
        if self.input_valid():
            self.iter_curenta = 1
            self.timer = QTimer()
            self.timer.setInterval(200)
            if self.btn_met_dreptunghiului.isChecked():
                self.timer.timeout.connect(self.plot_dreptunghiuri)
            elif self.btn_met_trapez.isChecked():
                self.timer.timeout.connect(self.plot_trapez)
            elif self.btn_met_simpson.isChecked():
                self.timer.timeout.connect(self.plot_simpson)
            else:
                self.afiseaza_eroare('Alegeti o metoda de calcul a integralei')
                return
            self.vizibilitate()
            self.timer.start()

    def input_valid(self):
        self.functie.setText(self.functie.text().replace('^', '**'))
        if self.validator_functie.validate(self.functie.text(), 0)[0] == QValidator.Invalid:
            return False
        try:
            if self.start_interval.text() == 'pi':
                self.a = np.pi
                if self.sfarsit_interval.text() == 'pi':
                    self.afiseaza_eroare('b trebuie sa fie mai mare decat a')
                    return False
                else:
                    self.b = float(self.sfarsit_interval.text())
            else:
                self.a = float(self.start_interval.text())
                if self.sfarsit_interval.text() == 'pi':
                    self.b = np.pi
                else:
                    self.b = float(self.sfarsit_interval.text())
            if self.a >= self.b:
                self.afiseaza_eroare('b trebuie sa fie mai mare decat a')
                return False
        except ValueError:
            self.afiseaza_eroare('a si b trebuie sa fie numere reale')
            return False
        try:
            self.limita = float(self.nr_iteratii.text())
            if self.limita >= 1 and self.limita.is_integer():
                self.limita = int(self.limita)
            if self.limita < 0:
                raise ValueError
        except ValueError:
            self.afiseaza_eroare('n trebuie sa ia valori intre 0 si 1 sau numar real')
            return False

        self.f = lambdify(Symbol('x'), self.functie.text())

        try:
            self.val_exacta.setText(str(quadrature(self.f, self.a, self.b)[0]))
        except:
            self.afiseaza_eroare('Functia nu este definita pe intervalul dat')
            return False

        return True

    def vizibilitate(self):
        for i in self.lista:
            i.show()

    def afiseaza_eroare(self, mesaj):
        msg = QMessageBox(parent=self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(mesaj)
        msg.setWindowTitle("Eroare")
        msg.exec_()

    def plot_dreptunghiuri(self):
        if self.iter_curenta == self.limita:
            self.timer.stop()
            self.iter_curenta = 1
            return
        self.iter_curenta += 1
        n = int(self.iter_curenta)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        nr_puncte = max(self.limita + 1, 150)
        gf = np.linspace(self.a, self.b, nr_puncte)
        ax.plot(gf, self.f(gf))

        x = np.linspace(self.a, self.b, n + 1)
        for i in range(n):
            f_mid = self.f(x[i] + (x[i + 1] - x[i]) / 2)
            xi = [x[i], x[i + 1], x[i + 1], x[i]]
            yi = [0, 0, f_mid, f_mid]
            ax.fill(xi, yi, color=(0.45, 0.57, 0.79, 0.45))
        ax.title.set_text('Nr subintervale: ' + str(n))
        self.canvas.draw()

        start = timeit.default_timer()
        try:

            if self.limita < 1:
                aprox, eroare = err_dreptunghi(self.functie.text(), self.a, self.b, n)
                self.timp_executie.setText(str(timeit.default_timer() - start))
                self.val_aprox.setText(str(aprox))
                if eroare > self.limita:
                    self.timer.stop()
                    self.iter_curenta = 1
                    return
            else:
                aprox = dreptunghiuri(self.f, self.a, self.b, n)
                durata = timeit.default_timer() - start
                self.timp_executie.setText(str(durata))
                self.val_aprox.setText(str(aprox))
        except Exception as e:
            print(e)

    def plot_trapez(self):
        if self.iter_curenta == self.limita:
            self.timer.stop()
            self.iter_curenta = 1
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        self.iter_curenta += 1
        n = int(self.iter_curenta)

        nr_puncte = max(self.limita + 1, 150)
        gf = np.linspace(self.a, self.b, nr_puncte)
        ax.plot(gf, self.f(gf))

        x = np.linspace(self.a, self.b, n + 1)
        for i in range(n):
            xi = [x[i], x[i + 1], x[i + 1], x[i]]
            yi = [0, 0, self.f(x[i + 1]), self.f(x[i])]
            ax.fill(xi, yi, color=(0.45, 0.57, 0.79, 0.45))
            ax.title.set_text('Nr subintervale: ' + str(n))
        self.canvas.draw()

        start = timeit.default_timer()
        if self.check_trapez_compozit.isChecked():
            aprox = trapez_compozit(self.f, self.a, self.b, n)
        else:
            aprox = trapez_clasic(self.f, self.a, self.b, n)
        durata = timeit.default_timer() - start
        self.val_aprox.setText(str(aprox))
        self.timp_executie.setText(str(durata))

    def plot_simpson(self):
        if self.iter_curenta == self.limita:
            self.timer.stop()
            self.iter_curenta = 1
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        self.iter_curenta += 1
        n = int(self.iter_curenta)

        # nr de puncte puncte a reprezenta functia
        nr_puncte = max(self.limita + 1, 150)
        # punctele
        grafic_functie = np.linspace(self.a, self.b, nr_puncte)
        # graficul functiei
        ax.plot(grafic_functie, self.f(grafic_functie))

        x = np.linspace(self.a, self.b, n + 1)
        for i in range(n):
            xi = [x[i], (x[i] + x[i + 1]) / 2,
                  x[i + 1]]
            yi = []
            for j in xi:
                yi.append(self.f(j))
            parabola = lagrange(xi, yi)

            a = x[i]
            mij = (x[i] + x[i + 1]) / 2
            b = x[i + 1]
            valori_a_mij = np.linspace(a, mij, 50)
            valori_mij_b = np.linspace(mij, b, 50)
            xi = [a, mij, b, a]
            yi = [0, 0, 0, parabola(a)]
            for j, k in zip(valori_mij_b, reversed(valori_a_mij)):
                xi.insert(3, j)
                xi.insert(-1, k)
                yi.insert(3, parabola(j))
                yi.insert(-1, parabola(k))
            ax.fill(xi, yi, color=(0.45, 0.57, 0.79, 0.45))
            ax.title.set_text("Nr intervale: " + str(n))
            self.canvas.draw()

        start = timeit.default_timer()
        if self.check_simpson_compozit.isChecked():
            aproximare = simpson_compozit(self.f, self.a, self.b, n)
        else:
            aproximare = simpson_clasic(self.f, self.a, self.b, n)
        durata = timeit.default_timer() - start
        self.val_aprox.setText(str(aproximare))
        self.timp_executie.setText(str(durata))

    def stop_animatie(self):
        if self.limita < 1:
            self.afiseaza_eroare('Numarul de iteratii trebuie sa fie nr integ.')
            return
        self.iter_curenta = self.limita - 1

    def citeste_fisier(self):
        # open file dialog and accept txt or csv files
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', "Text files (*.txt *.csv)")
        if fname[0]:
            with open(fname[0], 'r') as f:
                if f.name.endswith('.txt'):
                    fctii = f.read().splitlines()
                    functie = random.choice(fctii)
                    continut = functie.split(" ")
                else:
                    continut = f.readline().split(",")
                self.functie.setText(continut[0])
                self.start_interval.setText(continut[1])
                self.sfarsit_interval.setText(continut[2])
                self.nr_iteratii.setText(continut[3])


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("fusion")

    main = Fereastra()
    main.show()

    sys.exit(app.exec_())

# timp de executie
# eroarea
