import csv, codecs # base python, no pip install needed
import os # base python, no pip install needed
 
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport 
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile, Qt

import sys # base python, no pip install needed

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QVBoxLayout, QTextEdit
from PyQt5.uic import loadUi

from pathlib import Path # base python, no pip install needed

from healdata_utils.cli import convert_to_vlmd

#from frictionless import plugins # frictionless already installed as a healdata_utils dependency, no pip install needed
#from frictionless.plugins import remote
#from frictionless import describe

import pandas as pd # pandas already installed as a healdata_utils dependency, no pip install needed
import json # base python, no pip install needed
import pipe

import dsc_pkg_utils # local module, no pip install needed

###

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)

from layout_colorwidget import Color
#from layout_vlmdwidget import VLMDWindow
from layout_pkgtabswidget import PkgTabsWindow
from layout_vlmdtabswidget import VLMDTabsWindow
from layout_exptrktabswidget import ExpTrkTabsWindow
from layout_resourcetrktabswidget import ResourceTrkTabsWindow
from layout_resultstrktabswidget import ResultsTrkTabsWindow
#from layout_vlmdcreatewidget import VLMDCreateWindow
from layout_csveditwidget import CSVEditWindow

from layout_infotextbrowsewidget import InfoTextBrowserWindow

# this will prevent windows from setting the app icon to python automatically based on .py suffix
try:
    from ctypes import windll # only exists on windows, base python, no pip install needed
    myappid = 'mycompany.myproduct.subproduct.version' # somewhat arbitrary string, can set this to the recommendation but not really necessary
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DSC Data Packaging Tool - alpha")

        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        # Create a top-level layout
        self.layout = QVBoxLayout(self.main_widget)
        #self.setLayout(self.layout)
        
        self.workingDataPkgDirDisplayDefaultText = "Set a working data package directory! <br><br> Navigate to the \"Create or Continue Data Package\" sub-tab of the \"Data Package\" tab to set a new or existing data package directory as your working data package directory"
        self.workingDataPkgDirLabel = QLabel("Working Data Package Directory:", self)
        self.workingDataPkgDirDisplay = QtWidgets.QTextEdit(parent=self)
        self.workingDataPkgDirDisplay.setReadOnly(True)
        self.workingDataPkgDirDisplay.setText(self.workingDataPkgDirDisplayDefaultText)
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        tabs.addTab(PkgTabsWindow(workingDataPkgDirDisplay=self.workingDataPkgDirDisplay), "Data Package")
        tabs.addTab(ExpTrkTabsWindow(), "Experiment Tracker")
        tabs.addTab(ResourceTrkTabsWindow(), "Resource Tracker")
        tabs.addTab(VLMDTabsWindow(), "Data Dictionary")
        tabs.addTab(ResultsTrkTabsWindow(), "Results Tracker")
        
        #for n, color in enumerate(["red", "green", "blue", "yellow"]):
        #    tabs.addTab(Color(color), color)
        self.layout.addWidget(self.workingDataPkgDirLabel)
        self.layout.addWidget(self.workingDataPkgDirDisplay)
        self.layout.addWidget(tabs)
        
        #self.setCentralWidget(self.layout)


#app = QApplication(sys.argv)

#window = MainWindow()
#window.show()

#app.exec()

if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir,'heal-icon.ico')))
    app.setQuitOnLastWindowClosed(True) 
    #app.setApplicationName('DSC Data Packaging Tool - alpha')
   
    w = MainWindow()
    w.show()
   
    #main = MyWindow('')
    #main.setMinimumSize(820, 300)
    #main.setGeometry(0,0,820,700)
    #main.setWindowTitle("CSV Viewer")
    #main.show()
 
    sys.exit(app.exec_())