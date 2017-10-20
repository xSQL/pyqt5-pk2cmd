#!/usr/bin/env python3

import sys, os

from PyQt5.QtWidgets import QApplication, qApp, QFileDialog,\
    QTableWidgetItem as _t
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from inhx import Inhx8
from utils import functions as fn
from utils.pk2usb import Pk2USB

from gui import menu


class Window(object):
    """..."""
    def __init__(self):
        """..."""
        self.devfile = fn.read_device_file('PK2DeviceFile.dat')
        self.usb = Pk2USB(self.devfile)
        volts = self.usb.read_pk_voltages()
        self.usb.detect_device()
        print(volts)

        self.app = QApplication(sys.argv)
        self.ui = loadUi('gui/ui/main.ui')
        self.ui.setWindowTitle('PicKit2 - programmer')
        self.ui.actionOpen.triggered.connect(self.open_hex)
        self.ui.actionRead.triggered.connect(self.read_device)
        self.ui.actionExit.triggered.connect(qApp.quit)
        self.app.setWindowIcon(QIcon("gui/qrc/icon/icon.png"))
        self.ui.familyBox.currentIndexChanged.connect(self.change_family)
        self.ui.partsBox.currentIndexChanged.connect(self.change_part)
        self.ui.VddCheckBox.stateChanged.connect(self.vdd_state_changed)
        self.ui.VddSpinBox.valueChanged.connect(self.vdd_value_changed)
        self.ui.VddSpinBox.setValue(volts['vdd'])
        for family in self.devfile['Families']:
            self.ui.familyBox.addItem(family['FamilyName'])

    def vdd_state_changed(self, state, *args, **kwargs):
        """..."""
        if state:
            self.usb.vdd_on()
        else:
            self.usb.vdd_off()

    def vdd_value_changed(self, value, *args, **kwargs):
        self.usb.set_vdd_voltage(value, 0.85)

    def change_family(self, id):
        self.ui.partsBox.clear()
        part_list = [
            (p, p['PartName']) for p in self.devfile['Parts']\
            if p['Family']==id
        ]
        self.family = id
        self.part_list = [p[0] for p in part_list]
        self.part_name_list = [p[1] for p in part_list]
        self.ui.partsBox.addItems(self.part_name_list)

    def change_part(self, id):
        self.part = self.part_list[id]

        self.usb.device = self.part
        self.usb.family = self.family
        self.usb.download_part_scripts(self.family)
        self.init_program_table()
        self.init_ee_table()

    def read_device(self):
        print([hex(a) for a in self.usb.device_read()['memory']])
        print(self.devfile['Families'][self.usb.family])

    def init_program_table(self):
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
                _t('{:04x}'.format(i*8).upper())
             )

    def init_ee_table(self):
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

    def open_hex(self,):
        """..."""
        file = QFileDialog.getOpenFileName()

        inhx = Inhx8(file[0])

        data = inhx.getData()
        self.ui.dataTable.model().removeRows(0, self.ui.dataTable.rowCount());
        self.ui.dataTable.model().removeColumns(0, self.ui.dataTable.columnCount());    

        for i in range(9):
            self.ui.codeTable.insertColumn(i)
            self.ui.codeTable.setColumnWidth(i, 48)

        for i in range(128):
            self.ui.codeTable.insertRow(i)

        for j in range(128):
            self.ui.codeTable.setItem(
                j,
                0,
                _t('{:04x}'.format(j*8).upper())
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
