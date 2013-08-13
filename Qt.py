from PySide.QtCore import *
from PySide.QtGui import *
from UI import *
from FileIO import *
from Config import ConfigBorg
import sys
from TableView import MyTableView



class MyWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        #self.setGeometry(300, 200, 570, 450)
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QWidget(self)
        self.centralwidget.setMaximumSize(QSize(800, 559))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.lineEdit = QLineEdit(self.splitter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.tableView = MyTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.action_Open = QAction(self)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QAction(self)
        self.action_Save.setObjectName("action_Save")
        self.action_Exit = QAction(self)
        self.action_Exit.setObjectName("action_Exit")
        self.action_UndoFilter = QAction(self)
        self.action_UndoFilter.setObjectName("action_UndoFilter")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Edit.addAction(self.action_UndoFilter)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())

        self.retranslateUi()

        self.action_Open.triggered.connect(self.openFileMenuEvent)
        self.action_Save.triggered.connect(self.saveFileMenuEvent)
        self.action_UndoFilter.triggered.connect(self.undoFilterMenuEvent)


        self.status_progressbar=QProgressBar(self)
        self.statusbar.addPermanentWidget(self.status_progressbar)

        self.tableView.verticalScrollBar().valueChanged.connect(lambda val: self.status_progressbar.setValue(val))
        self.tableView.verticalScrollBar().rangeChanged.connect(lambda min,max: self.status_progressbar.setRange(min,max))

        #self.setWindowTitle("CSV viewer")
        f_p = r"D:\LocalData\a189493\Desktop\servers_daily_01.csv"
        self.openFile(f_p)
        #table_model = TableModel(self, f_p)
        #self.table_model = table_model
        #table_view = MyTableView()
        #self.table_view = table_view
        #self.tableView.setModel(table_model)
        #layout = QVBoxLayout(self)
        #layout.addWidget(table_view)
        #self.setLayout(layout)

    def test(self, *args):
        print args

    def undoFilterMenuEvent(self, *args):
        filter_dialog = FilterHistoryDialog(self)
        filter_dialog.show()


    def openFile(self,f_p):
        """
        Open requested file in listview
        """
        self.statusbar.showMessage("Opening %s (computing line offsets)"%f_p)
        table_model = TableModel(self, f_p)
        self.table_model = table_model
        self.tableView.setModel(table_model)
        self.statusbar.showMessage("Done")
        self.status_progressbar.setFormat("%p% - %v/%m lines")
        #self.status_progressbar.setRange(1, self.table_model.rowCount(self))
        #self.status_progressbar.setValue(1)
        self.status_progressbar.setTextVisible(True)

    def openFileMenuEvent(self, *args):
        logging.debug("open file requested")
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file') #3rd optional arg : drirectory
        if fname is None or fname == u'':
            logging.warning("No file selected")
            return False
        logging.debug("Opening %s"%(fname))
        self.openFile(fname)

    def saveFileMenuEvent(self, *args):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file")
        if filename is None or filename == u"":
            logging.warning("No filename selected")
            return False
        self.statusbar.showMessage("Saving to %s" % (filename))
        self.tableView.model().save(filename)
        self.statusbar.showMessage("Done")

    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
        self.pushButton.setText(QApplication.translate("MainWindow", "PushButton", None, QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QApplication.translate("MainWindow", "&File", None, QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QApplication.translate("MainWindow", "&Edit", None, QApplication.UnicodeUTF8))
        self.action_Open.setText(QApplication.translate("MainWindow", "&Open", None, QApplication.UnicodeUTF8))
        self.action_Save.setText(QApplication.translate("MainWindow", "&Save", None, QApplication.UnicodeUTF8))
        self.action_Save.setShortcut(QApplication.translate("MainWindow", "Ctrl+S", None, QApplication.UnicodeUTF8))
        self.action_Exit.setText(QApplication.translate("MainWindow", "&Exit", None, QApplication.UnicodeUTF8))
        self.action_UndoFilter.setText(QApplication.translate("MainWindow", "&UndoFilter", None, QApplication.UnicodeUTF8))

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()