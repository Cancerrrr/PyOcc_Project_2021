from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from Main.main import Ui_MainWindow
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
        self.setWindowTitle("压力容器设计计算系统")
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

        self.display.FitAll()

        self.window.pushButton_generation.clicked.connect(self.pushButton_generation_clicked)
        self.window.pushButton_clear.clicked.connect(self.clear_display)

    def pushButton_generation_clicked(self):
        print(self.sender().text()+"点了")
        a_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
        self.display.ResetView()
        self.display.DisplayShape(a_box, update=True)

    def clear_display(self):
        print(self.sender().text() + "点了")
        self.display.EraseAll()









