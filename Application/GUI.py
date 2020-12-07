from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget,  QPushButton, QLineEdit, QLabel, QTextEdit, QFormLayout, QTableView, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
import mysql.connector as sql

class App(QWidget):

    def __init__(self):
        
        super(App, self).__init__()
        self.setWindowTitle('Login')
        self.configure_gui()
        self.create_widgets()
        self.show()

    def configure_gui(self):
        
        self.setMinimumSize(300, 200)
        self.layout = QVBoxLayout(self)
        self.label = QLabel('Enter credentials')
        self.label.setAlignment(Qt.AlignCenter)
        self.form = QFormLayout()

    def create_widgets(self):
        
        for text in [
            'Hostname:', 'Database:', 'Username:', 'Password:'
            ]:
            widget = QLineEdit(self)
            widget.returnPressed.connect(self.check_login)
            self.form.addRow(text, widget)
        else:
            button = QPushButton('Submit')
            button.pressed.connect(self.check_login)
            self.form.addWidget(button)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.form)

    def check_login(self, event=None):
        
        try:
            credentials = {
                'host': self.form.itemAt(1).widget().text(),
                'database': self.form.itemAt(3).widget().text(),
                'user': self.form.itemAt(5).widget().text(),
                'password': self.form.itemAt(7).widget().text()
                }
            Main(credentials)
            self.close()

        except:
            QMessageBox().warning(
                self, 'Wrong credentials', 'You have entered the wrong credentials'
                )

    def keyPressEvent(self, event):
    
        key_press = event.key()
        modifiers = event.modifiers()
        alt = modifiers == Qt.AltModifier

        if key_press == Qt.Key_Escape: self.close()

class Main(QMainWindow):
    
    def __init__(self, credentials):
        
        super(Main, self).__init__()
        self.setWindowTitle('Application')
        self.configure_gui()
        self.create_widgets(credentials)
        self.showMaximized()

    def configure_gui(self):

        self.center = QWidget(self)
        self.layout = QVBoxLayout()
        self.center.setLayout(self.layout)
        self.setCentralWidget(self.center)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.setFixedHeight(25)

    def create_widgets(self, credentials):
        
        self.connect = MySql(self, credentials)
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
    
    def __init__(self, parent, creds):

        self.parent = parent
        self.DATAB = sql.connect(**creds)
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