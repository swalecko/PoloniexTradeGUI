from PyQt5 import QtSql, QtGui


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')

    db.setDatabaseName('C:\\Users\\swalecko\\Documents\\PoloniexTradeGUI\\database.db')
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                QtGui.qApp.tr("Unable to establish a database connection.\n"
                              "This example needs SQLite support. Please read "
                              "the Qt SQL driver documentation for information "
                              "how to build it.\n\n"
                              "Click Cancel to exit."),
                QtGui.QMessageBox.Cancel)
        return False
    
    query = QtSql.QSqlQuery()
    query.exec_("create table dborder(id int primary key, "
                "ordernumber varchar(20), type varchar(20), price varchar(20), samount varchar(20), amount varchar(20)) ")
    #query.exec_("insert into dborder values(1, '123413095', 'buy', '0.00181000', '100.00', '97.00')")

    query.exec_("insert into dborder values(2, '223413095', 'sell', '0.00181000', '100.00', '97.00')")

    return True
