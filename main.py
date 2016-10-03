#!/usr/bin/env python3

import sys, os

from PyQt5.QtWidgets import QApplication, qApp, QFileDialog,\
    QTableWidgetItem as _t
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

from inhx import Inhx8

from gui import menu
import area


class Window(object):
    """..."""
    def __init__(self):
        """..."""
        self.app = QApplication(sys.argv)
        self.ui = loadUi('gui/ui/main.ui')
        self.ui.setWindowTitle('PicKit2')
        self.ui.actionOpen.triggered.connect(self.openHex)
        self.ui.actionExit.triggered.connect(qApp.quit)
        self.app.setWindowIcon(QIcon("icon/icon.png"))

    def openHex(self,):
        """..."""
        file = QFileDialog.getOpenFileName()

        inhx = Inhx8(file[0])

        data = inhx.getData()

        try:
            self.ui.deviceLabel.setText(
                str(''.join([data[8199][0], data[8199][1]]))
            )
        except Exception as e:
            print(e)
            pass

        for i in range(9):
            self.ui.codeTable.insertColumn(i)
            self.ui.codeTable.setColumnWidth(i, 48)

        for i in range(128):
            self.ui.codeTable.insertRow(i)

        for j in range(128):
            self.ui.codeTable.setItem(
                j,
                0,
                _t(str(hex(j*8)))
            )
            for i in range(8):
                a = j*8+i;

                b = data.get(a)

                if b:
                    item = ''.join([data[a][0], data[a][1]])
                else:
                    item = '3FFF'

                self.ui.codeTable.setItem(
                    j,
                    i+1,
                    _t(item)
                )


if __name__=="__main__":
    w = Window()
    w.ui.show()
    sys.exit(w.app.exec_())
