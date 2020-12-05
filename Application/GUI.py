import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget,  QPushButton, QTextEdit, QTableView, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel
import mysql.connector as sql

class MySql:
    
    def __init__(self):

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
            
            except sql.errors.DatabaseError: 
                
                self.reconnect()

        return list()

    def reconnect(self, attempts=5, time=15):

        self.DATAB.reconnect(attempts, time)

    def commit(self): self.DATAB.commit()
    
    def close(self): self.DATAB.close()

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
        
        self.connect = MySql()
        self.textfield = QTextEdit(self)
        self.enter = QPushButton('Enter', self)
        self.enter.pressed.connect(self.execute_query)
        self.table = QTableView(self)

        self.layout.addWidget(self.textfield)
        self.layout.addWidget(self.enter)
        self.layout.addWidget(self.table)

    def execute_query(self):

        statement = self.textfield.toPlainText()
        rows = self.connect.execute(statement, fetch=1)
        columns = self.connect.CURSOR.column_names
        self.table.update(rows)
        self.statusbar.showMessage(
            f'{len(rows)} row(s) returned'
            )
    
    def keyPressEvent(self, event):
    
        key_press = event.key()
        modifiers = event.modifiers()
        alt = modifiers == Qt.AltModifier

        if key_press == Qt.Key_Escape: self.close()

class Table(QTableView):

    def __init__(self, parent): 
        
        super(Table, self).__init__(parent)
        self.model = Model(self)   
        self.setModel(self.model)
        
    def configure_gui(self): pass

    def create_widgets(self): pass

    def update(self, rows): self.model.rows = rows

class Model(QAbstractTableModel):
    
    def __init__(self, parent):

        QAbstractTableModel.__init__(self, parent)
        self.rows = []
        
    # def flags(self, index): return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def rowCount(self, parent=None): return len(self.rows)

    def columnCount(self, parent=None): return len(self.rows[0])

    def data(self, index, role): pass
        
if __name__ == '__main__':

    Qapp = QApplication(sys.argv)
    app = App()
    Qapp.exec_()