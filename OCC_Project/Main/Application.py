import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from Main.main_3dview import MainWindowView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindowView()
    main_window.show()
    sys.exit(app.exec_())