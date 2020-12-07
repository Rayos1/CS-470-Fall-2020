from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget,  QPushButton, QTextEdit, QTableView, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
import mysql.connector as sql

class App(QMainWindow):
    
    def __init__(self):
        
        super(App, self).__init__()
        self.setWindowTitle('Application')
        self.configure_gui()
        self.create_widgets()
        self.showMaximized()

    def configure_gui(self):

        self.center = QWidget()
        self.layout = QVBoxLayout()
        self.center.setLayout(self.layout)
        self.setCentralWidget(self.center)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.setFixedHeight(25)

    def create_widgets(self):
        
        self.connect = MySql(self)
        self.textfield = QTextEdit(self)
        self.textfield.setMaximumHeight(250)
        self.textfield.setPlaceholderText('Enter query')
        self.enter = QPushButton('Enter', self)
        self.enter.pressed.connect(self.execute_query)
        self.table = Table(self)

        self.layout.addWidget(self.textfield)
        self.layout.addWidget(self.enter)
        self.layout.addWidget(self.table)

    def execute_query(self):

        statements = self.textfield.toPlainText().split(';')

        for statement in statements:
            
            self.table.update(
                self.connect.execute(statement, fetch=1),
                self.connect.CURSOR.column_names
                )
            self.statusbar.showMessage(
                f'{len(self.table.model.rows)} row(s) returned'
                )
    
    def keyPressEvent(self, event):
    
        key_press = event.key()
        modifiers = event.modifiers()
        alt = modifiers == Qt.AltModifier

        if key_press == Qt.Key_Escape: self.close()

class MySql(object):
    
    def __init__(self, parent):

        self.parent = parent
        self.DATAB = sql.connect(option_files='credentials.ini')
        self.CURSOR = self.DATAB.cursor(buffered=True)

    def execute(self, statement, arguments=None, many=0, commit=0, fetch=0):

        for _ in range(10):
            try:
                if many: self.CURSOR.executemany(statement, arguments)
                else: self.CURSOR.execute(statement, arguments)

                if commit: return self.DATAB.commit()
                if fetch: return self.CURSOR.fetchall()
                return list()
            
            except sql.errors.ProgrammingError as error:

                QMessageBox().warning(self.parent, 'Program Error', error.msg)
                break
            
            except sql.errors.DatabaseError: 
                
                self.reconnect()

        return list()

    def reconnect(self, attempts=5, time=15):

        self.DATAB.reconnect(attempts, time)

    def commit(self): self.DATAB.commit()
    
    def close(self): self.DATAB.close()

class Table(QTableView):
    
    def __init__(self, parent):
        
        super(Table, self).__init__(parent)
        self.model = Model(self)   
        self.setModel(self.model)

    def update(self, rows, columns):

        self.model.rows = rows
        if not rows: columns = []
        self.model.columns = columns
        self.model.layoutChanged.emit()

class Model(QAbstractTableModel):
    
    def __init__(self, parent):

        QAbstractTableModel.__init__(self, parent)
        self.rows = self.columns = []
        
    def rowCount(self, parent=None): return len(self.rows)

    def columnCount(self, parent=None): return len(self.columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columns[section]

        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role): 

        if role == Qt.DisplayRole:
            
            return str(self.rows[index.row()][index.column()])

        return QVariant()
    
if __name__ == '__main__':

    Qapp = QApplication([])
    app = App()
    Qapp.exec_()