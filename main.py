import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ReadXpert")
    app.setFont(QFont("Microsoft YaHei", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
