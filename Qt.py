from PySide.QtCore import *
from PySide.QtGui import *
from FileIO import *
from Config import ConfigBorg
import sys
from TableView import MyTableView



class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setGeometry(300, 200, 570, 450)
        self.setWindowTitle("CSV viewer")
        f_p = r"D:\LocalData\a189493\Desktop\servers_daily_01.csv"
        table_model = TableModel(self, f_p)
        self.table_model = table_model
        table_view = MyTableView()
        self.table_view = table_view
        table_view.setModel(table_model)
        #table_header_view = QHeaderView(Qt.Horizontal, table_view)
        #QComboBox()
        #table_view.setHorizontalHeader(table_header_view)
        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.setLayout(layout)



def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()