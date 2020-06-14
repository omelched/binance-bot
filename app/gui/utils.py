from typing import Union

from PyQt5 import QtWidgets


def iterate_Qt_items(layout):
    result = []
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if type(item) == QtWidgets.QWidgetItem:
            result.append(item.widget())
        else:
            result.append(item)
            result.extend(iterate_Qt_items(item))

    return result


def get_text_from_widget(widget: Union[QtWidgets.QLineEdit, QtWidgets.QComboBox]) -> str:
    if type(widget) == QtWidgets.QLineEdit:
        return widget.text()
    elif type(widget) == QtWidgets.QComboBox:
        return widget.currentText()
    else:
        raise Exception
