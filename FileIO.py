import sys
import logging
import re
import math
from operator import itemgetter
from PySide.QtCore import *
logging.basicConfig(level=logging.DEBUG)

class TableModel(QAbstractTableModel):
    def __init__(self, parent, f_p, *args):
        self.file_io = FileIO(f_p)
        QAbstractTableModel.__init__(self, parent, *args)
        self.initial_sort = 2

    def rowCount(self, parent):
        return self.file_io.rowCount()

    def columnCount(self, parent):
        return self.file_io.columnCount()

    def data(self, index, role = Qt.DisplayRole):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return self.file_io.data(index.row(), index.column())
        return None

    def setData(self, index, value):
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def sort(self, column, order):
        if self.initial_sort == 0:
            self.file_io.sort(column, order)
            self.modelReset.emit()
            #TODO datachanged signal
            #TODO sort order
        else:
            self.initial_sort -= 1

    def save(self, path):
        """
        Save current filtered file to disk
        """
        logging.debug("Saving to %s" % (path))
        self.file_io.save(path)

    def revertToFilter(self,id):
        """
        Restore state to given filter id
        """
        self.file_io.revertToFilter(id)

    def filter(self, pattern, column=-1, exact=False, mode="exclude"):
        self.file_io.filter(column, pattern, exact, mode)
        self.modelReset.emit()

    def filterkeypressed(self, *args):
        if (len(args) == 1) and (len(args[0]) == 3):
            filter = args[0][0]
            selected_text = args[0][1]
            column = args[0][2]
            if filter['column'] == "any":
                column = -1
            logging.debug("Filtering %s on %s exact = %s"%(selected_text, column, filter['exact']))
            if "mode" in filter:
                self.filter(pattern=selected_text, column=column, exact=filter['exact'], mode=filter['mode'])
            else:
                self.filter(pattern=selected_text, column=column, exact=filter['exact'])

    def listFilters(self):
        """
        Returns applied filters
        """
        filters = []
        total = self.file_io.initialRowCount()
        for f in self.file_io.data_row_offset_map:
            filters.append(
                {
                    'name': f['operation'],
                    'id': f['id'],
                    'lines': len(f['row_offsets']),
                    'pcent': 100*len(f['row_offsets'])/total,
                }
            )
        return filters

class FileIO():
    #you must implement rowCount(), columnCount(), and data(row,collumn)
    def __init__(self, f_p):
        self.f = open(f_p, 'r')
        self.line_offsets = []
        self.data_row_offset_map = []
        """ contains : {
            'operation':'',
            'row_offsets':[(),(),]
        }"""
        self.RAM_CACHE_SIZE = 10
        self.computeLineOffset()
        self.ram_cache = []
        self.SEPARATOR = ";"
        self.cached_lines =(0,0)
        self.column_count = None


    def revertToFilter(self,id):
        """
        Restore state to given filter id
        """
        filter = [d for d in self.data_row_offset_map if d['id'] == int(id)][0]
        logging.debug("Reverting to filter %s : %s" % (id, filter['operation']))
        self.data_row_offset_map.append(filter)

    def computeLineOffset(self):
        logging.debug("Computing line offsets")
        current_offset = 0
        line_offsets = []
        for line in self.f:
            line_offsets.append( (current_offset, len(line)) )
            current_offset += len(line)
        fileorder = {
            'operation':'fileorder',
            'row_offsets':line_offsets,
            'id': 0,
        }
        self.data_row_offset_map.append(fileorder)
        logging.debug("Done")

    def getLineOffsets(self):
        return self.data_row_offset_map[-1]['row_offsets']

    def rowCount(self):
        row_count = len(self.getLineOffsets())
        return row_count

    def initialRowCount(self):
        """
        return row count before any filtering
        """
        row_count = len(self.data_row_offset_map[0]['row_offsets'])
        return row_count

    def columnCount(self):
        if self.column_count != None:
            return self.column_count
        else:
            self.column_count = len(self.getRow(0).split(self.SEPARATOR))
            return self.column_count

    def getRowAsArray(self, row):
        row = self.getRow(row)
        row_array = row.split(self.SEPARATOR)
        return row_array

    def data(self, row, column):
        #logging.debug("%s,%s requested"%(row,column))
        #row = self.getRow(row)
        #value = row.split(self.SEPARATOR, column + 1)[column]
        value = self.getRowAsArray(row)[column]
        return value

    def sort(self, column, order):
        #Sort based on collumns
        sort = [] #[(value, (offset,len))]
        base_offsets = self.getLineOffsets()
        for i in range(self.rowCount()):
            sort.append( (self.data(i, column), base_offsets[i]) ) # We sort on row value, take base_offsets as the result
        sort = sorted(sort,key=itemgetter(0))
        row_offsets = []
        for i in sort:
            row_offsets.append(i[1])
        sort = None
        self.data_row_offset_map.append(
            {
                'operation':'sort%s'%(column),
                'row_offsets':row_offsets,
                'id': max([d['id'] for d in self.data_row_offset_map]) + 1,
            }
        )

    def filterre(self, column, pattern, exact=False):
        regex = (re.escape(pattern))
        regex_c = re.compile(regex)
        base_offsets = self.getLineOffsets()
        row_offsets = []
        for i in range(self.rowCount()):
            if exact == True:
                if column == -1:
                    if pattern in self.getRowAsArray(i):
                        continue
                else:
                    if regex_c.match(self.data(i,column)) != None:
                        continue
            else:
                if column == -1:
                    #Fuzzy search on all columns
                    if regex_c.search(self.getRow(i)) != None:
                        continue
                else:
                    #Fuzzy search on one column
                    if regex_c.search(self.data(i,column)) != None:
                        continue
            # Append rows that did not match
            row_offsets.append(base_offsets[i])
        # Save result in offset map
        self.data_row_offset_map.append(
            {
                'operation':'filter%s%s%s'%(column, pattern, exact),
                'row_offsets':row_offsets
            }
        )

    def save(self, path):
        """
        Save current filtered file to disk
        """
        f = open(path, 'wb')
        for i in range(self.rowCount()):
            row = self.getRow(i)
            f.write(row)
        f.close()


    def filter(self, column, pattern, exact=False, mode="exclude"):
        # Remove every line with a collumns containing pattern
        # TODO Test with regex for speed, non exact using wildcard, multiple patterns ursing OR, compile once execute many
        base_offsets = self.getLineOffsets()
        row_offsets = []
        column_count = self.columnCount()
        for i in range(self.rowCount()):
            if column == -1:
                #Line based
                if exact == False:
                    if pattern in self.getRow(i):
                        continue
                else:
                    #Exact value in any column
                    if pattern in self.getRowAsArray(i):
                        continue
            else:
                #One column -> 1 value
                value = self.data(i, column)
                if (value == pattern) or ((exact == False) and (pattern in value)):
                    continue
            # Keep the row if no match
            row_offsets.append(base_offsets[i])
        if mode == "include":
            # If include instead of exclude, reverse the selection
            row_offsets = list(set(base_offsets) - set(row_offsets))
        self.data_row_offset_map.append(
            {
                'operation':'filter%s%s%s'%(column, pattern, exact),
                'row_offsets':row_offsets,
                'id': max([d['id'] for d in self.data_row_offset_map]) + 1,
            }
        )
        pass


    def getRow(self, row):
        row_offset, row_len= self.getLineOffsets()[row]
        self.f.seek(row_offset)
        return self.f.read(row_len)

"""    def getChunk(self, line_start, line_end):
        line_start_offset = self.line_offsets[line_start - 1]
        line_end_offset = self.line_offsets[line_end - 1]
        self.f.seek(line_start_offset)
        if (line_end - line_start) <= self.RAM_CACHE_SIZE:
            # Put everything in cache
            self.ram_cache =  self.f.read(line_end_offset - line_start_offset).splitlines()
            self.cached_lines = (line_start, line_end)
            for l in self.ram_cache:
                yield l
        else:
            #Put what we can in ram, then get the rest without caching it
            for i in range( int(math.ceil((line_end - line_start) / float(self.RAM_CACHE_SIZE))) ):
                self.ram_cache = self.f.read(self.RAM_CACHE_SIZE).splitlines()
                #Will overflow a bit
                for l in self.ram_cache:
                    yield l"""

if __name__ == '__main__':
    #f_p = sys.argv[1]
    f_p = r"D:\LocalData\a189493\Desktop\servers_daily_01.csv"
    fio = FileIO(f_p)
    print fio.data(10,0)
    print fio.data(12825,0)
    print fio.rowCount()
    print fio.columnCount()