import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import mysql.connector as sql

class CONNECT:
    
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

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Application')
        self.configure_gui()
        self.create_widgets()
        self.showMaximized()

    def configure_gui(self): 

        l = QLabel('My simple app.')
        l.setAlignment(Qt.AlignCenter)
        l.setMargin(10)
        l.setStyleSheet('font: 30px')

        self.setCentralWidget(l)

    def create_widgets(self): pass
        
        # self.connect = CONNECT()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()