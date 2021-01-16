import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI import Main
from UI import disk_design_dialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Main.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())