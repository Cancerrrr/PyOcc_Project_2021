from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from ui_test.test import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem
from pythonocc_canvas.qtDisplay import qtViewer3d
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import*

from OCC.Display.backend import load_backend
load_backend('qt-pyqt5')
import OCC.Display.qtDisplay as qtDisplay

class MainWindowView(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.window = Ui_MainWindow()
        self.window.setupUi(self)
        self.init_view()

    def init_view(self):
        # 设置canvas
        self.canva = qtDisplay.qtViewer3d(self)
        # 显示设置
        self.canva.InitDriver()  # canva的驱动,设置驱动后，才能成功display
        self.display = self.canva._display
        self.rgb_list1 = [206, 215, 222]
        self.rgb_list2 = [128, 128, 128]
        self.display.set_bg_gradient_color(self.rgb_list1, self.rgb_list2)  # 设置背景渐变色
        self.display.display_triedron()  # 设置黑色画布
        # 在widget中加入画布
        self.window.canva_area.layout().addWidget(self.canva)
        a_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
        self.ais_box = self.display.DisplayShape(a_box)[0]
        self.display.FitAll()
        # 设置程序图标
        self.setWindowTitle("压力容器")









