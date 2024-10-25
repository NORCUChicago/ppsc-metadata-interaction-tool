#https://realpython.com/python-pyqt-layout/#:~:text=addTab()%20%2C%20then%20that%20icon,layout%20containing%20the%20required%20widgets.

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

#from layout_vlmdcreatewidget import VLMDCreateWindow
#from layout_exptrkaddwidget import ExpTrkAddWindow
from layout_termtrkaddwidget import TermTrkAddWindow
from layout_csvviewpushtoloadwidget import CSVViewPushToLoadWindow
#from layout_csvpushtoloadwidget import CSVPushToLoadWindow
from layout_infotextwidget import InfoTextWindow

class TermTrkTabsWindow(QWidget):
    def __init__(self, workingDataPkgDirDisplay):
        super().__init__()
        self.setWindowTitle("Term Tracker")
        #self.resize(270, 110)
        self.workingDataPkgDirDisplay = workingDataPkgDirDisplay
        
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.infoText = "You'll create a single term tracker for your study and add one entry per term that is part of your study. This will provide a clear overview of what terms are used in the study, what they mean, and how terms have been added or modified over the course of the study. This will facilitate continuity and passed-down knowledge within study groups, and sharing and re-use of the data and knowledge produced by your study outside of the original study group."
        
        
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(InfoTextWindow(self.infoText), "Info")
        tabs.addTab(TermTrkAddWindow(workingDataPkgDirDisplay=self.workingDataPkgDirDisplay), "Add Term")
        tabs.addTab(CSVViewPushToLoadWindow(workingDataPkgDirDisplay=self.workingDataPkgDirDisplay,fileBaseName="term-tracker.csv",fileStartsWith="", fileTypeTitle="Term Tracker"), "View Tracker")
        
                
        layout.addWidget(tabs)

    # def generalTabUI(self):
    #     """Create the General page UI."""
    #     generalTab = QWidget()
    #     layout = QVBoxLayout()
    #     layout.addWidget(QCheckBox("General Option 1"))
    #     layout.addWidget(QCheckBox("General Option 2"))
    #     generalTab.setLayout(layout)
    #     return generalTab

    # def networkTabUI(self):
    #     """Create the Network page UI."""
    #     networkTab = QWidget()
    #     layout = QVBoxLayout()
    #     layout.addWidget(QCheckBox("Network Option 1"))
    #     layout.addWidget(QCheckBox("Network Option 2"))
    #     networkTab.setLayout(layout)
    #     return networkTab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpTrkTabsWindow()
    window.show()
    sys.exit(app.exec_())



