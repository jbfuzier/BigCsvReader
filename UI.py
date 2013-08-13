from PySide.QtCore import *
from PySide.QtGui import *


class FilterHistoryDialog(QDialog):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        layout = QVBoxLayout(self)
        self.filter_model = self.parent().tableView.model()
        self.filterlist = QTreeWidget(self)
        self.filterlist.setColumnCount(4)
        #item = QTreeWidgetItem(self.filterlist, "test", 0)
        #self.filterlist.addTopLevelItem(item)
        self.populate()
        self.filterlist.itemDoubleClicked.connect(self.filterSelected)
        layout.addWidget(self.filterlist)
        self.setLayout(layout)

    def filterSelected(self, *args):
        id = args[0].data(0,0)
        self.filter_model.revertToFilter(id)
        self.close()

    def populate(self):
        h =  self.filterlist.headerItem()
        h.setText(0, "Id")
        h.setText(1, "Operation")
        h.setText(2, "Lines")
        h.setText(3, "Pcent of total")
        for f in self.filter_model.listFilters():
            item = QTreeWidgetItem(self.filterlist)
            item.setText(0, str(f['id']))
            item.setText(1, f['name'])
            item.setText(2, str(f['lines']))
            item.setText(3, str(f['pcent']))
            self.filterlist.addTopLevelItem(item)
