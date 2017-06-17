#!/usr/bin/env python3

import sys, os

from PyQt5.QtWidgets import QApplication, qApp, QFileDialog,\
    QTableWidgetItem as _t
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from inhx import Inhx8
from utils import functions as fn


from gui import menu


class Window(object):
    """..."""
    def __init__(self):
        """..."""
        self.devfile = fn.read_device_file('PK2DeviceFile.dat')
        print(self.devfile['scripts'][3])
        self.app = QApplication(sys.argv)
        self.ui = loadUi('gui/ui/main.ui')
        self.ui.setWindowTitle('PicKit2 - programmer')
        self.ui.actionOpen.triggered.connect(self.openHex)
        self.ui.actionExit.triggered.connect(qApp.quit)
        self.app.setWindowIcon(QIcon("gui/qrc/icon/icon.png"))
        
        self.ui.familyBox.currentIndexChanged.connect(self.changeFamily)
        self.ui.partsBox.currentIndexChanged.connect(self.changePart)        
        
        for family in self.devfile['families']:
            self.ui.familyBox.addItem(family['family_name'])
                
    def changeFamily(self, id):
        self.ui.partsBox.clear()
        part_list = [
            (p, p['part_name']) for p in self.devfile['parts']\
            if p['family']==id
        ]
        self.part_list = [p[0] for p in part_list]
        self.part_name_list = [p[1] for p in part_list]
        self.ui.partsBox.addItems(self.part_name_list)

    def changePart(self, id):
        self.part = self.part_list[id]
        self.initProgramTable()
        self.initEETable()

    def initProgramTable(self):
        #Clear table
        self.ui.codeTable.model().removeRows(0, self.ui.codeTable.rowCount());
        self.ui.codeTable.model().removeColumns(0, self.ui.codeTable.columnCount());        
        
        for i in range(9):
            self.ui.codeTable.insertColumn(i)
            self.ui.codeTable.setColumnWidth(i, 48)
        self.ui.codeTable.setColumnWidth(0, 64)

        for i in range(int(self.part['ProgramMem']/8)):
            self.ui.codeTable.insertRow(i)
            self.ui.codeTable.setItem(
                i,
                0,
                _t(str(hex(i*8)))
            )            
        
    def initEETable(self):
        #Clear table
        self.ui.dataTable.model().removeRows(0, self.ui.dataTable.rowCount());
        self.ui.dataTable.model().removeColumns(0, self.ui.dataTable.columnCount());        
        
        for i in range(9):
            self.ui.dataTable.insertColumn(i)
            self.ui.dataTable.setColumnWidth(i, 48)
        self.ui.dataTable.setColumnWidth(0, 64)

        for i in range(int(self.part['EEMem']/8)):
            self.ui.dataTable.insertRow(i)
            self.ui.dataTable.setItem(
                i,
                0,
                _t(str(hex(self.part['EEAddr']+i*8)))
            )            
        
    def openHex(self,):
        """..."""
        file = QFileDialog.getOpenFileName()

        inhx = Inhx8(file[0])

        data = inhx.getData()


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
