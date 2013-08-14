from PySide.QtCore import *
from PySide.QtGui import *



class MyHeaderView(QHeaderView):
    def __init__(self, parent):
        QHeaderView.__init__(self, Qt.Horizontal, parent)
        self.setMovable(True)
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)
        self.boxes = []

    def handleSectionMoved(self, *args):
        logical, oldVisualIndex, newVisualIndex = args
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            box = self.boxes[logical]
            box.setGeometry(self.sectionViewportPosition(logical), 10, self.sectionSize(logical) - 10, self.height())

    def handleSectionResized(self, *args):
        i=args[0]
        for j in range(self.visualIndex(i), self.count()):
            logical = self.logicalIndex(j)
            box = self.boxes[logical]
            box.setGeometry(self.sectionViewportPosition(logical), 10, self.sectionSize(logical) - 10, self.height())

    def fixComboPositions(self):
        for i in range(self.count()):
            box = self.boxes[i]
            box.setGeometry(self.sectionViewportPosition(i), 10, self.sectionSize(i) - 10, self.height())

    def showWidgets(self):
        for i in range(self.count()):
            if len(self.boxes) <= i:
                box = QComboBox(self)
                self.boxes.append(box)
            self.boxes[i].setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 10, self.height())
            self.boxes[i].addItem("testA%s" % i,0)
            self.boxes[i].addItem("testB%s" % i,0)
            self.boxes[i].show()





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




