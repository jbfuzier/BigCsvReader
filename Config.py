from PySide.QtCore import Qt
class ConfigBorg:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
    # and whatever else you want in your class -- that's all!

    auto_apply_filter = True
    first_line_as_header_title = False
    delimiter = u";"
    edit_filters = [
                    {
                                'key':Qt.Key_R,
                                'exact':False,
                                'column':"any",
                                'name':"Excludes lines whith a column LIKE *pattern*",
                    },
                    {
                                'key':Qt.Key_E,
                                'exact':True,
                                'column':"any",
                                'name':"Excludes lines with a column == pattern",
                    },
                    {
                                'key':Qt.Key_F,
                                'exact':False,
                                'column':"current",
                                'name':"Excludes lines with this column LIKE *pattern*",
                    },
                    {
                                'key':Qt.Key_G,
                                'exact':True,
                                'column':"current",
                                'name':"Exclude lines where this column == pattern",
                    },

                    {
                        'key':Qt.Key_I,
                        'exact':True,
                        'column':"current",
                        'name':"Includes only lines with this column == pattern",
                        'mode':'include',
                    },
                    {
                        'key':Qt.Key_O,
                        'exact':False,
                        'column':"current",
                        'name':"Include only lines with this column LIKE *pattern*",
                        'mode':'include',
                    },

                    {
                        'key':Qt.Key_P,
                        'exact':True,
                        'column':"any",
                        'name':"Includes only lines with a column == pattern",
                        'mode':'include',
                        },
                    {
                        'key':Qt.Key_M,
                        'exact':False,
                        'column':"any",
                        'name':"Include only lines with a column LIKE *pattern*",
                        'mode':'include',
                    },
    ]

    table_filters = [
                    {
                                'key':Qt.Key_R,
                                'exact':True,
                                'column':"any",
                                'name':"Excludes lines where a column == pattern",
                    },
                    {
                                'key':Qt.Key_G,
                                'exact':True,
                                'column':"current",
                                'name':"Excludes lines where this column == pattern",
                    },
                    {
                                'key':Qt.Key_I,
                                'exact':True,
                                'column':"current",
                                'name':"Includes only lines where this column == pattern",
                                'mode':'include',
                    },
                    {
                                'key':Qt.Key_O,
                                'exact':False,
                                'column':"current",
                                'name':"Include only lines where this column LIKE *pattern*",
                                'mode':'include',
                    },

                    {
                                'key':Qt.Key_P,
                                'exact':True,
                                'column':"any",
                                'name':"Includes only lines where a column == pattern",
                                'mode':'include',
                                },
                    {
                                'key':Qt.Key_M,
                                'exact':False,
                                'column':"any",
                                'name':"Include only lines with a column LIKE *pattern*",
                                'mode':'include',
                    },

    ]