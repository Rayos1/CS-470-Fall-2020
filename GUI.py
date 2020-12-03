from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox, QStatusBar, QGroupBox, QPushButton, QAction, QSizePolicy
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