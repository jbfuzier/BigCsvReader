
from PySide.QtCore import *
from PySide.QtGui import *
from FileIO import *
from Config import ConfigBorg
import sys
from UI import *

class MyTableView(QTableView):
    """
     Custom Tableview allows to filter shortcuts keys on cells
    """
    KeyPressed = Signal(object)
    def __init__(self, *args):
        QTableView.__init__(self, *args)
        self.config = ConfigBorg()
        delegate = TextEditDelegate(self)
        self.setItemDelegate(delegate)
        self.setCornerButtonEnabled(False)
        font = QFont("Courier New", 14)
        self.setFont(font)
        #table_view.resizeColumnsToContents() #Scan whole table, not efficient
        self.setSortingEnabled(True) #TODO Sorting on demand only, prevent table scan
        #table_header_view = self.horizontalHeader()
        #table_header_view.setMovable(True)
        my_table_header_view = MyHeaderView(self)
        self.setHorizontalHeader(my_table_header_view)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        #table_view.connect(table_view, SIGNAL("customContextMenuRequested(const QPoint)"), self, SLOT("test()"))
        self.customContextMenuRequested.connect(self.MyCustomContextMenu)


    def scrollContentsBy(self, *args, **kwargs):
        QTableView.scrollContentsBy(self, *args, **kwargs)
        dx = args[0]
        if dx != 0:
            self.horizontalHeader().fixComboPositions()

    def setModel(self, *args, **kwargs):
        QTableView.setModel(self, *args, **kwargs)
        self.KeyPressed.connect(self.model().filterkeypressed)
        self.horizontalHeader().showWidgets()

    def keyPressEvent(self, event, *args):
        keys = [e['key'] for e in self.config.table_filters]
        if (event.key()in keys):
            selected_index = self.selectionModel().selectedIndexes()[0]
            pattern = self.model().data(selected_index)
            filter = [f for f in self.config.table_filters if f['key'] == event.key()][0]
            self.KeyPressed.emit((filter, pattern, selected_index.column()))
            return True
        QTableView.keyPressEvent(self, event, *args)


    def MyCustomContextMenu(self):
        print "test"
        menu = QMenu(self)
        for filter in self.config.table_filters:
            filter_action = QAction(filter['name'], menu)
            filter_action.triggered.connect(lambda f=filter: self.MyCustomContextMenuEvent(f))
            menu_item = menu.addAction(filter_action)
        menu.exec_(QCursor().pos())

    def MyCustomContextMenuEvent(self, event, *args):
        try:
            selected_index = self.selectionModel().currentIndex()
        except Exception as e:
            logging.warning("No cell selected : %s" % e)
            return False
        pattern = self.model().data(selected_index)
        filter = [f for f in self.config.table_filters if f == event][0]
        self.KeyPressed.emit((filter, pattern, selected_index.column()))
        return True



class MyQTextEdit(QTextEdit):
    """
        Implement Key shortcuts grabbing on a text edit (Custom edit fields inside the tabble)
    """

    KeyPressed = Signal(object)

    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        self.config = ConfigBorg()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.MyCustomContextMenu)

    def event(self, event):
        keys = [e['key'] for e in self.config.edit_filters]
        if (event.type()==QEvent.KeyPress) and (event.key()in keys):
            #self.emit(SIGNAL("Key_RPressed"))
            logging.debug("Key %s pressed and grabbed"%event.key())
            selected_text = self.textCursor().selectedText()
            if len(selected_text)==0:
                logging.warning("Nothing selected, cannot filter!")
            filter = [f for f in self.config.edit_filters if f['key'] == event.key()]
            if filter == None or len(filter) != 1:
                logging.error("Could not find a filter entry for this key")
                return True
            filter = filter[0]
            table_view = self.parent().parent()
            selected_indexes = table_view.selectionModel().selectedIndexes()
            if len(selected_indexes)!=1:
                logging.error("To many or no selected indexes")
                return True
            column = selected_indexes[0].column()
            self.KeyPressed.emit((filter, selected_text, column))
            logging.debug("Selected text : %s"%selected_text)
        return True
        #return QLineEdit.event(self, event) # Default actiosn for other keys

    def MyCustomContextMenu(self):
        menu = QMenu(self)
        for filter in self.config.edit_filters:
            filter_action = QAction(filter['name'], menu)
            filter_action.triggered.connect(lambda f=filter: self.MyCustomContextMenuEvent(f))
            menu.addAction(filter_action)
        menu.exec_(QCursor().pos())

    def MyCustomContextMenuEvent(self, event, *args):
        selected_text = self.textCursor().selectedText()
        if len(selected_text)==0:
            logging.warning("Nothing selected, cannot filter!")
        filter = [f for f in self.config.edit_filters if f == event]
        if filter == None or len(filter) != 1:
            logging.error("Could not find a filter entry for this key")
            return True
        filter = filter[0]
        table_view = self.parent().parent()
        selected_indexes = table_view.selectionModel().selectedIndexes()
        if len(selected_indexes)!=1:
            logging.error("To many or no selected indexes")
            return True
        column = selected_indexes[0].column()
        self.KeyPressed.emit((filter, selected_text, column))
        logging.debug("Selected text : %s"%selected_text)
        return True

class TextEditDelegate(QItemDelegate):
    """
    Custom text edit mode for Qtableview, allows to listen for key events and get selected text inside the cell
    """
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def createEditor(self,parent,option,index):
        text = MyQTextEdit(parent)
        table_view=self.parent()
        table_model=table_view.model()
        #text.connect(text, SIGNAL("Key_RPressed"), table_model, SLOT("filterkeypressed()"))
        text.KeyPressed.connect(table_model.filterkeypressed)
        #text.KeyRPressed.connect(lambda: table_model.filterkeypressed("test"))
        return text
