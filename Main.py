#!/usr/bin/python


__author__ = 'mediator'

from PyQt5.QtWidgets import QApplication, qApp, QFileDialog, QGraphicsScene
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import sys, menu, area


class Window():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = loadUi('main.ui')
        self.ui.setWindowTitle('PicKit2 simple programmer')
        self.ui.actionOpen.triggered.connect(self.openHex)
        self.ui.actionExit.triggered.connect(qApp.quit)
        self.app.setWindowIcon(QIcon("icon/icon.png"))

    def openHex(self):
        file = QFileDialog.getOpenFileName()
        with open(file[0], 'r') as f:
            content = f.readlines()

        for l in content:
            line = l[1:-1]
            data = line[8:-1]
            list = [data[i:i+2] for i in range(0, len(data), 2)]
            list = list + ['FF' for i in range(0, 17-len(list))]
            chars = '</span><span style="width: 32px; margin-left: 10px;">'.join(list)
            s = '<b style="color: red">%s:</b> <span style="margin-left: 10px; width: 32px">%s</span>'%(line[2:6], chars)
            self.ui.textBrowser.append(s)




w = Window()
w.ui.show()
sys.exit(w.app.exec_())