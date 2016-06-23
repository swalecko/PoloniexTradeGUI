import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt5 import QtCore, QtGui, QtSql, QtWidgets

import connection


class EditableSqlModel(QtSql.QSqlQueryModel):
    def flags(self, index):
        flags = super(EditableSqlModel, self).flags(index)

        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemIsEditable

        return flags


    def refresh(self):
        self.setQuery('select * from dborder')
        model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Order Number")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "Type")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "Price(BTC)")
        model.setHeaderData(4, QtCore.Qt.Horizontal, "SAmount(XMR)")
        model.setHeaderData(5, QtCore.Qt.Horizontal, "Amount(XMR)")



def initializeModel(model):
    model.setQuery('select * from dborder')
    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Order Number")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Type")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Price(BTC)")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "SAmount(XMR)")
    model.setHeaderData(5, QtCore.Qt.Horizontal, "Amount(XMR)")




offset = 0
views = []

def createView(title, model):
    global offset, views

    view = QtWidgets.QTableView()
    views.append(view)
    view.setModel(model)
    view.setWindowTitle(title)
    view.move(100 + offset, 100 + offset)
    view.resizeColumnsToContents()
    view.verticalHeader().hide()
    offset += 20
    view.show()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    editableModel = EditableSqlModel()
    initializeModel(editableModel)
    createView("Editable Query Model", editableModel)

    sys.exit(app.exec_())