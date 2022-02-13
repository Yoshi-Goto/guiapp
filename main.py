import sys

import MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow
from MainWindow import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui_window = Ui_MainWindow()
    ui_window.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
