from PySide.QtCore import *
from PySide.QtGui import *
import logging
from FileIO import TableModel
from Config import ConfigBorg

class OpenFileUISequence():
    def __init__(self, mainwindows):
        self.mainwindows = mainwindows
        self.config = ConfigBorg()
        self.selectFile()

    def selectFile(self, *args):
        logging.debug("open file requested")
        fname, _ = QFileDialog.getOpenFileName(self.mainwindows, 'Open file') #3rd optional arg : drirectory
        if fname is None or fname == u'':
            logging.warning("No file selected")
            return False
        logging.debug("Opening %s"%(fname))
        open_option = OpenOptionDialog(self.mainwindows)
        if open_option.exec_() == 1:
            self.config.auto_apply_filter = open_option.AutoApplyFilterscheckBox.isChecked()
            self.config.first_line_as_header_title = open_option.headerTitleCheckBox.isChecked()
            self.config.delimiter = open_option.delimiterLineEdit.text()
            self.config.file_charset = self.config.charsets[open_option.CharsetComboBox.currentText()]
            #TODO : Handle chardet analysys here
            self.openFile(fname)
            return True
        else:
            return False


    def openFile(self,f_p):
        """
        Open requested file in listview
        """
        self.mainwindows.statusbar.showMessage("Opening %s (computing line offsets)"%f_p)
        table_model = TableModel(self.mainwindows, f_p)
        self.mainwindows.table_model = table_model
        self.mainwindows.tableView.setModel(table_model)
        self.mainwindows.statusbar.showMessage("Done")
        self.mainwindows.status_progressbar.setFormat("%p% - %v/%m lines")
        #self.status_progressbar.setRange(1, self.table_model.rowCount(self))
        #self.status_progressbar.setValue(1)
        self.mainwindows.status_progressbar.setTextVisible(True)


class OpenOptionDialog(QDialog):
    def __init__(self, *args):
        self.config = ConfigBorg()
        QDialog.__init__(self, *args)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delimiterLineEdit = QLineEdit(self)
        self.delimiterLineEdit.setObjectName("delimiterLineEdit")
        self.horizontalLayout.addWidget(self.delimiterLineEdit)
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerTitleCheckBox = QCheckBox(self)
        self.headerTitleCheckBox.setChecked(self.config.first_line_as_header_title)
        self.headerTitleCheckBox.setObjectName("headerTitleCheckBox")
        self.verticalLayout.addWidget(self.headerTitleCheckBox)
        self.AutoApplyFilterscheckBox = QCheckBox(self)
        self.AutoApplyFilterscheckBox.setChecked(self.config.auto_apply_filter)
        self.AutoApplyFilterscheckBox.setObjectName("AutoApplyFilterscheckBox")
        self.verticalLayout.addWidget(self.AutoApplyFilterscheckBox)
        self.CharsetComboBox = QComboBox(self)
        self.CharsetComboBox.addItems(self.config.charsets.keys())
        #self.AutoApplyFilterscheckBox.setChecked(self.config.auto_apply_filter)
        self.CharsetComboBox.setObjectName("CharsetComboBox")
        self.verticalLayout.addWidget(self.CharsetComboBox)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi()
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate("Dialog", "Dialog", None, QApplication.UnicodeUTF8))
        self.delimiterLineEdit.setText(QApplication.translate("Dialog", ";", None, QApplication.UnicodeUTF8))
        self.label.setText(QApplication.translate("Dialog", "Columns Delimiter", None, QApplication.UnicodeUTF8))
        self.headerTitleCheckBox.setText(QApplication.translate("Dialog", "First Line as Header Title", None, QApplication.UnicodeUTF8))
        self.AutoApplyFilterscheckBox.setText(QApplication.translate("Dialog", "Auto Apply Filers", None, QApplication.UnicodeUTF8))


    def filterSelected(self, *args):
        id = args[0].data(0,0)
        self.filter_model.revertToFilter(id)
        self.close()

    def populate(self):
        pass
