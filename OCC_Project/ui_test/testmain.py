import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from ui_test import test_view
from ui_test.test_view import MainWindowView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = test.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    main_window = MainWindowView()
    main_window.show()
    sys.exit(app.exec_())