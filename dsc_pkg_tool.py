# issues: 
# copy only copies the last value
# paste pastes everything into each highlighted cell

# tutorial on using table view/model together:
# https://doc.qt.io/qt-5/modelview.html
# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
# https://www.pythonguis.com/faq/adding-qcombobox-to-a-qtableview-and-getting-setting-values-after-creation/
# https://stackoverflow.com/questions/30457935/pyqt4-adding-combobox-in-qtableview

# guidance on how to create a user input form
# https://www.geeksforgeeks.org/pyqt5-create-a-user-form-to-get-information/

# using code here as main starting point for window that allows load, edit, save of csv
# https://python-forum.io/thread-1785.html
# https://github.com/Axel-Erfurt/TreeView/blob/master/Qt5_CSV.py

# may be helpful with implementing validation/drop downs in qtableview csv editor
# https://stackoverflow.com/questions/6571209/how-to-display-drop-down-in-column-of-qtableview-and-filter-based-on-drop-down

# guidance on adding header to qtableview/qstandarditemmodel
# https://stackoverflow.com/questions/42094545/cant-set-and-display-a-qtabelview-horizontal-header
# https://stackoverflow.com/questions/37222081/pyqt-qtableview-set-horizontal-vertical-header-labels
# https://stackoverflow.com/questions/17478993/how-to-change-headers-title-of-a-qtableview

# using this here for example of how to open a new window from main window
# https://www.pythonguis.com/tutorials/creating-multiple-windows/

# this helped with guidance on why qpushbuttons were not showing up in main window
# https://stackoverflow.com/questions/37304684/qwidgetsetlayout-attempting-to-set-qlayout-on-mainwindow-which-already

# guidance on using qtextedit (better replacement in this context for qlineedit)
# https://stackoverflow.com/questions/16568451/pyqt-how-to-make-a-textarea-to-write-messages-to-kinda-like-printing-to-a-co

# guidance on packaging with pyinstaller
# https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/

# guidance on packaging with fbs 
# https://www.pythonguis.com/tutorials/packaging-pyqt5-apps-fbs/
# fbs tutorial
# https://github.com/mherrmann/fbs-tutorial
# fbs manual
# https://build-system.fman.io/manual/

# not used here but may be useful later
# https://realpython.com/python-menus-toolbars/

#!/usr/bin/python3
#-*- coding:utf-8 -*-
import csv, codecs # base python, no pip install needed
import os # base python, no pip install needed
 
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport 
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile, Qt

import sys # base python, no pip install needed

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

from pathlib import Path # base python, no pip install needed

from healdata_utils.cli import convert_to_vlmd

from frictionless import plugins # frictionless already installed as a healdata_utils dependency, no pip install needed
from frictionless.plugins import remote
from frictionless import describe

import pandas as pd # pandas already installed as a healdata_utils dependency, no pip install needed
import json # base python, no pip install needed
import requests # requests already installed as a healdata_utils dependency, no pip install needed
import pipe

import dsc_pkg_utils # local module, no pip install needed

# this will prevent windows from setting the app icon to python automatically based on .py suffix
try:
    from ctypes import windll # only exists on windows, base python, no pip install needed
    myappid = 'mycompany.myproduct.subproduct.version' # somewhat arbitrary string, can set this to the recommendation but not really necessary
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

basedir = os.path.dirname(__file__)
 
class MyWindow(QtWidgets.QWidget):
   def __init__(self, fileName, parent=None):
       super(MyWindow, self).__init__(parent)
       self.fileName = ""
       self.fname = "Liste"
       self.myColNames = []
       self.model =  QtGui.QStandardItemModel(self)
 
       self.tableView = QtWidgets.QTableView(self)
       self.tableView.setStyleSheet(stylesheet(self))
       self.tableView.setModel(self.model)
       self.tableView.horizontalHeader().setStretchLastSection(True)
       self.tableView.setShowGrid(True)
       self.tableView.setGeometry(10, 50, 780, 645)
       #self.model.dataChanged.connect(self.finishedEdit)
 
       self.pushButtonLoad = QtWidgets.QPushButton(self)
       self.pushButtonLoad.setText("Load CSV")
       self.pushButtonLoad.clicked.connect(self.loadCsv)
       self.pushButtonLoad.setFixedWidth(80)
       self.pushButtonLoad.setStyleSheet(stylesheet(self))
 
       self.pushButtonWrite = QtWidgets.QPushButton(self)
       self.pushButtonWrite.setText("Save CSV")
       self.pushButtonWrite.clicked.connect(self.writeCsv)
       self.pushButtonWrite.setFixedWidth(80)
       self.pushButtonWrite.setStyleSheet(stylesheet(self))
 
       self.pushButtonPreview = QtWidgets.QPushButton(self)
       self.pushButtonPreview.setText("Print Preview")
       self.pushButtonPreview.clicked.connect(self.handlePreview)
       self.pushButtonPreview.setFixedWidth(80)
       self.pushButtonPreview.setStyleSheet(stylesheet(self))
 
       self.pushButtonPrint = QtWidgets.QPushButton(self)
       self.pushButtonPrint.setText("Print")
       self.pushButtonPrint.clicked.connect(self.handlePrint)
       self.pushButtonPrint.setFixedWidth(80)
       self.pushButtonPrint.setStyleSheet(stylesheet(self))
 
       self.pushAddRow = QtWidgets.QPushButton(self)
       self.pushAddRow.setText("add Row")
       self.pushAddRow.clicked.connect(self.addRow)
       self.pushAddRow.setFixedWidth(80)
       self.pushAddRow.setStyleSheet(stylesheet(self))
 
       self.pushDeleteRow = QtWidgets.QPushButton(self)
       self.pushDeleteRow.setText("delete Row")
       self.pushDeleteRow.clicked.connect(self.removeRow)
       self.pushDeleteRow.setFixedWidth(80)
       self.pushDeleteRow.setStyleSheet(stylesheet(self))
 
       self.pushAddColumn = QtWidgets.QPushButton(self)
       self.pushAddColumn.setText("add Column")
       self.pushAddColumn.clicked.connect(self.addColumn)
       self.pushAddColumn.setFixedWidth(80)
       self.pushAddColumn.setStyleSheet(stylesheet(self))
 
       self.pushDeleteColumn = QtWidgets.QPushButton(self)
       self.pushDeleteColumn.setText("delete Column")
       self.pushDeleteColumn.clicked.connect(self.removeColumn)
       self.pushDeleteColumn.setFixedWidth(86)
       self.pushDeleteColumn.setStyleSheet(stylesheet(self))
 
       self.pushClear = QtWidgets.QPushButton(self)
       self.pushClear.setText("Clear")
       self.pushClear.clicked.connect(self.clearList)
       self.pushClear.setFixedWidth(60)
       self.pushClear.setStyleSheet(stylesheet(self))
 
       grid = QtWidgets.QGridLayout()
       grid.setSpacing(10)
       grid.addWidget(self.pushButtonLoad, 0, 0)
       grid.addWidget(self.pushButtonWrite, 0, 1)
       grid.addWidget(self.pushAddRow, 0, 2)
       grid.addWidget(self.pushDeleteRow, 0, 3)
       grid.addWidget(self.pushAddColumn, 0, 4)
       grid.addWidget(self.pushDeleteColumn, 0, 5)
       grid.addWidget(self.pushClear, 0, 6)
       grid.addWidget(self.pushButtonPreview, 0, 7)
       grid.addWidget(self.pushButtonPrint, 0, 8, 1, 1, QtCore.Qt.AlignRight)
       grid.addWidget(self.tableView, 1, 0, 1, 9)
       self.setLayout(grid)
 
       item = QtGui.QStandardItem()
       self.model.appendRow(item)
       self.model.setData(self.model.index(0, 0), "", 0)
       #self.tableView.resizeColumnsToContents()
 
   def loadCsv(self, fileName):
       fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
               (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
 
       if fileName:
           print(fileName)
           #ff = open(fileName, 'r')
           #mytext = ff.read()
#            print(mytext)
           #ff.close()
           f = open(fileName, 'r',newline='')
           with f:
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)

                reader = csv.reader(f, delimiter = ',')
                self.model.clear()

                # list to store the names of columns
                list_of_column_names = []
                # row counter; set to zero
                i=0

                for row in reader:
                    if i==0:
                        # adding the first row to list of column names
                        list_of_column_names.append(row)
                        print(list_of_column_names)
                        print(list_of_column_names[0])
                        # iterate the counter so no longer zero
                        i+=1
                    else:
                        # adding all rows except first row as rows to model
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)

                i=0 # reset counter back to zero 

                self.myColNames = list_of_column_names[0] 
                self.model.setHorizontalHeaderLabels(self.myColNames)  
                #self.model.setHorizontalHeaderLabels(list_of_column_names[0])
                
                header = self.tableView.horizontalHeader()
                header.setDefaultAlignment(Qt.AlignHCenter)
                #self.tableView.setModel(self.model)
                #self.tableView.resizeColumnsToContents()



   def writeCsv(self, fileName):
       # find empty cells
       for row in range(self.model.rowCount()):
           for column in range(self.model.columnCount()):
               myitem = self.model.item(row,column)
               if myitem is None:
                   item = QtGui.QStandardItem("")
                   self.model.setItem(row, column, item)
       fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                       (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),"CSV Files (*.csv)")
       if fileName:
           print(fileName)
           f = open(fileName, 'w')
           with f:
               writer = csv.writer(f, delimiter = ',', lineterminator='\r')
               writer.writerow(self.myColNames)
               for rowNumber in range(self.model.rowCount()):
                   fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                        QtCore.Qt.DisplayRole)
                    for columnNumber in range(self.model.columnCount())]
                   writer.writerow(fields)
               self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
               self.setWindowTitle(self.fname)
 
   def handlePrint(self):
       dialog = QtPrintSupport.QPrintDialog()
       if dialog.exec_() == QtWidgets.QDialog.Accepted:
           self.handlePaintRequest(dialog.printer())
 
   def handlePreview(self):
       dialog = QtPrintSupport.QPrintPreviewDialog()
       dialog.setFixedSize(1000,700)
       dialog.paintRequested.connect(self.handlePaintRequest)
       dialog.exec_()
 
   def handlePaintRequest(self, printer):
       # find empty cells
       for row in range(self.model.rowCount()):
           for column in range(self.model.columnCount()):
               myitem = self.model.item(row,column)
               if myitem is None:
                   item = QtGui.QStandardItem("")
                   self.model.setItem(row, column, item)
       printer.setDocName(self.fname)
       document = QtGui.QTextDocument()
       cursor = QtGui.QTextCursor(document)
       model = self.tableView.model()
       table = cursor.insertTable(model.rowCount(), model.columnCount())
       for row in range(table.rows()):
           for column in range(table.columns()):
               cursor.insertText(model.item(row, column).text())
               cursor.movePosition(QtGui.QTextCursor.NextCell)
       document.print_(printer)
 
   def removeRow(self):
       model = self.model
       indices = self.tableView.selectionModel().selectedRows() 
       for index in sorted(indices):
           model.removeRow(index.row()) 
 
   def addRow(self):
       item = QtGui.QStandardItem("")
       self.model.appendRow(item)
 
   def clearList(self):
       self.model.clear()
 
   def removeColumn(self):
       model = self.model
       indices = self.tableView.selectionModel().selectedColumns() 
       for index in sorted(indices):
           model.removeColumn(index.column()) 
 
   def addColumn(self):
       count = self.model.columnCount()
       print (count)
       self.model.setColumnCount(count + 1)
       self.model.setData(self.model.index(0, count), "", 0)
       #self.tableView.resizeColumnsToContents()
 
   def finishedEdit(self):
       self.tableView.resizeColumnsToContents()
       
 
   def contextMenuEvent(self, event):
       self.menu = QtWidgets.QMenu(self)
       # copy
       copyAction = QtWidgets.QAction('Copy', self)
       copyAction.triggered.connect(lambda: self.copyByContext(event))
       # paste
       pasteAction = QtWidgets.QAction('Paste', self)
       pasteAction.triggered.connect(lambda: self.pasteByContext(event))
       # cut
       cutAction = QtWidgets.QAction('Cut', self)
       cutAction.triggered.connect(lambda: self.cutByContext(event))
       # delete selected Row
       removeAction = QtWidgets.QAction('delete Row', self)
       removeAction.triggered.connect(lambda: self.deleteRowByContext(event))
       # add Row after
       addAction = QtWidgets.QAction('insert new Row after', self)
       addAction.triggered.connect(lambda: self.addRowByContext(event))
       # add Row before
       addAction2 = QtWidgets.QAction('insert new Row before', self)
       addAction2.triggered.connect(lambda: self.addRowByContext2(event))
       # add Column before
       addColumnBeforeAction = QtWidgets.QAction('insert new Column before', self)
       addColumnBeforeAction.triggered.connect(lambda: self.addColumnBeforeByContext(event))
       # add Column after
       addColumnAfterAction = QtWidgets.QAction('insert new Column after', self)
       addColumnAfterAction.triggered.connect(lambda: self.addColumnAfterByContext(event))
       # delete Column
       deleteColumnAction = QtWidgets.QAction('delete Column', self)
       deleteColumnAction.triggered.connect(lambda: self.deleteColumnByContext(event))
       # add other required actions
       self.menu.addAction(copyAction)
       self.menu.addAction(pasteAction)
       self.menu.addAction(cutAction)
       self.menu.addSeparator()
       self.menu.addAction(addAction)
       self.menu.addAction(addAction2)
       self.menu.addSeparator()
       self.menu.addAction(addColumnBeforeAction)
       self.menu.addAction(addColumnAfterAction)
       self.menu.addSeparator()
       self.menu.addAction(removeAction)
       self.menu.addAction(deleteColumnAction)
       self.menu.popup(QtGui.QCursor.pos())
 
   def deleteRowByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row()
           self.model.removeRow(row)
           print("Row " + str(row) + " deleted")
           self.tableView.selectRow(row)
 
   def addRowByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row() + 1
           self.model.insertRow(row)
           print("Row at " + str(row) + " inserted")
           self.tableView.selectRow(row)
 
   def addRowByContext2(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row()
           self.model.insertRow(row)
           print("Row at " + str(row) + " inserted")
           self.tableView.selectRow(row)
 
   def addColumnBeforeByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           col = i.column()
           self.model.insertColumn(col)
           print("Column at " + str(col) + " inserted")
 
   def addColumnAfterByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           col = i.column() + 1
           self.model.insertColumn(col)
           print("Column at " + str(col) + " inserted")
 
   def deleteColumnByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           col = i.column()
           self.model.removeColumn(col)
           print("Column at " + str(col) + " removed")
 
   def copyByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row()
           col = i.column()
           myitem = self.model.item(row,col)
           if myitem is not None:
               clip = QtWidgets.QApplication.clipboard()
               clip.setText(myitem.text())
 
   def pasteByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row()
           col = i.column()
           myitem = self.model.item(row,col)
           clip = QtWidgets.QApplication.clipboard()
           myitem.setText(clip.text())
 
   def cutByContext(self, event):
       for i in self.tableView.selectionModel().selection().indexes():
           row = i.row()
           col = i.column()
           myitem = self.model.item(row,col)
           if myitem is not None:
               clip = QtWidgets.QApplication.clipboard()
               clip.setText(myitem.text())
               myitem.setText("")
 
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        
        widget = QtWidgets.QWidget()
        
        self.buttonNewPkg = QtWidgets.QPushButton(text="Create New HEAL-DSC Data Package",parent=self)
        self.buttonNewPkg.clicked.connect(self.create_new_pkg)

        self.buttonInferHealCsvDd = QtWidgets.QPushButton(text="CSV Data >> HEAL CSV Data Dictionary",parent=self)
        self.buttonInferHealCsvDd.clicked.connect(self.csv_data_infer_dd)

        self.buttonConvertRedcapCsvDd = QtWidgets.QPushButton(text="Redcap CSV Data Dictionary >> HEAL CSV Data Dictionary",parent=self)
        self.buttonConvertRedcapCsvDd.clicked.connect(self.redcap_csv_dd_convert)
        #self.buttonConvertRedcapCsvDd.setFixedSize(100,60)

        self.buttonEditCsv = QtWidgets.QPushButton(text="View/Edit CSV", parent=self)
        self.buttonEditCsv.clicked.connect(self.show_new_window)
        #self.setCentralWidget(self.buttonEditCsv)
        #self.buttonEditCsv.setFixedSize(100,60)

        self.buttonValidateHealCsvDd = QtWidgets.QPushButton(text="Validate HEAL CSV Data Dictionary", parent=self)
        #self.buttonValidateHealCsvDd.setFixedSize(100,60)

        # maybe switch Line edit to this: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPlainTextEdit.html#more
        #self.userMessageBox = QtWidgets.QLineEdit(parent=self)
        self.userMessageBox = QtWidgets.QTextEdit(parent=self)
        self.userMessageBox.setReadOnly(True)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.buttonNewPkg)
        layout.addWidget(self.buttonInferHealCsvDd)
        layout.addWidget(self.buttonConvertRedcapCsvDd)
        layout.addWidget(self.buttonEditCsv)
        layout.addWidget(self.buttonValidateHealCsvDd)
        layout.addWidget(self.userMessageBox)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_new_pkg(self):
        #file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #folder = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        #filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Hey! Select a File')
        parentFolderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Parent Directory Where Data Package Should Be Created!')
        pkgPath = dsc_pkg_utils.new_pkg(pkg_parent_dir_path=parentFolderPath)

        messageText = 'Created new HEAL DSC data package at: ' + pkgPath
        self.userMessageBox.setText(messageText)

    def csv_data_infer_dd(self):
        ifileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
               (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")

        ifname = os.path.splitext(str(ifileName))[0].split("/")[-1]
        
        messageText = 'Inferring minimal data dictionary from: ' + ifileName
        self.userMessageBox.setText(messageText)

        first_dd_df = dsc_pkg_utils.infer_dd(ifileName)

        messageText = messageText + '\n\n\n' + 'Success!'
        self.userMessageBox.setText(messageText)

        ofileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                       (QtCore.QDir.homePath() + "/" + ifname + ".csv"),"CSV Files (*.csv)")

        messageText = messageText + '\n\n\n' + 'Populating HEAL CSV data dictionary template with values from inferred data dictionary.' + '\n\n\n' + 'Output data dictionary in HEAL CSV data dictionary format will be saved as: ' + ofileName
        self.userMessageBox.setText(messageText)

        second_dd_df = dsc_pkg_utils.add_dd_to_heal_dd_template(first_dd_df,required_first=True,save_path=ofileName)

        messageText = messageText + '\n\n\n' + 'Success!'
        self.userMessageBox.setText(messageText)


    def redcap_csv_dd_convert(self):
        fname,_=QtWidgets.QFileDialog.getOpenFileName(self,'Select Input Redcap CSV Data Dictionary file',QtCore.QDir.homePath())
        #fname=QtWidgets.QFileDialog.getOpenFileName(self,'Open file',QtCore.QDir.homePath())
        #path = fname[0]

        print(fname)
        print(type(fname))
        print(Path(fname))
        print(type(Path(fname)))

        outputFolderPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Directory Where HEAL CSV Data Dictionary Should Be Saved!')
        
        print(outputFolderPath)

        #redcap_path = Path(path)
        #redcap_output = redcap_path.parent.with_name('output')
        #self.userMessageBox.setText('Converting: '  + path + '\n\n\n' + 'Output path: ' + redcap_output.__str__())

        convert_to_vlmd(
            #filepath=redcap_path,
            #filepath=fname,
            filepath=Path(fname),
            outputdir=outputFolderPath,
            data_dictionary_props={
                "title":"my dd title",
                "description":"my dd description"
            },
            inputtype="redcap.csv"
        )
#  
#        to_json(
#            filepath=redcap_path,
#            outputdir=redcap_output,
#            data_dictionary_props={
#                "title":"my dd title",
#                "description":"my dd description"
#            },
#            inputtype="redcap.csv"
#        )
#
#        to_csv_from_json(redcap_output/redcap_path.with_suffix(".json").name,redcap_output)


    def show_new_window(self,checked):
        if self.w is None:
            self.w = MyWindow('')
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


def stylesheet(self):
       return """
       QTableView
       {
border: 1px solid grey;
border-radius: 0px;
font-size: 12px;
        background-color: #f8f8f8;
selection-color: white;
selection-background-color: #00ED56;
       }
 
QTableView QTableCornerButton::section {
    background: #D6D1D1;
    border: 1px outset black;
}
 
QPushButton
{
font-size: 11px;
border: 1px inset grey;
height: 24px;
width: 80px;
color: black;
background-color: #e8e8e8;
background-position: bottom-left;
} 
 
QPushButton::hover
{
border: 2px inset goldenrod;
font-weight: bold;
color: #e8e8e8;
background-color: green;
} 
"""
 
if __name__ == "__main__":
   import sys
 
   app = QtWidgets.QApplication(sys.argv)
   app.setWindowIcon(QtGui.QIcon(os.path.join(basedir,'heal-icon.ico')))
   #app.setApplicationName('MyWindow')
   
   w = MainWindow()
   w.show()
   
   #main = MyWindow('')
   #main.setMinimumSize(820, 300)
   #main.setGeometry(0,0,820,700)
   #main.setWindowTitle("CSV Viewer")
   #main.show()
 
sys.exit(app.exec_())