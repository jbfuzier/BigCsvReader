from PySide.QtCore import *
from PySide.QtGui import *



class MyHeaderView(QHeaderView):
    def __init__(self, parent):
        QHeaderView.__init__(self, Qt.Horizontal, parent)
        self.setMovable(True)
        self.quick_filter = False
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
        if self.quick_filter == True:
            for i in range(self.count()):
                box = self.boxes[i]
                box.setGeometry(self.sectionViewportPosition(i), 10, self.sectionSize(i) - 10, self.height())

    def showWidgets(self, autofilter):
        if self.quick_filter == True:
            for i in range(self.count()):
                if len(self.boxes) <= i:
                    box = QComboBox(self)
                    self.boxes.append(box)
                self.boxes[i].setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 10, self.height())
                self.boxes[i].addItem("%s"%i, 0)
                for value, occurences in autofilter[i]: #TODO Sort by count
                    self.boxes[i].addItem("%s (%s)" % (value, occurences),0)
                self.boxes[i].show()
                self.boxes[i].currentIndexChanged[int].connect(lambda arg,i=i: self.quickFilterChange(arg, i))

    #@Slot(str)
    def quickFilterChange(self, *args):
        print args
        index = args[0]-1 #Because of title as first entry in dropdown list
        if index < 0:
            return False
        column = args[1]
        value = self.parent().model().autoFilter()[column][index][0]
        self.parent().model().filter(value, column=column, exact=True, mode="include")

    def enableQuickFilter(self):
        self.quick_filter = True #TODO FIXME Handle quick filyter toogle state on the MODEL!!
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)
        #TODO find a more elegant way to deal with messages
        #self.parent().parent().statusbar.showMessage("Computing/Populating autofilter lists")
        autofilter = self.parent().model().autoFilter()
        self.showWidgets(autofilter)
        #self.parent().parent().statusbar.showMessage("Done")


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




