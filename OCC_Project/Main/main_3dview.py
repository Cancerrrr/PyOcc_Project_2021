from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from Main.main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem
from PyQt5.QtWidgets import *
from OCC.Display.backend import load_backend

from Model_Generation import Elliptical

load_backend('qt-pyqt5')
import OCC.Display.qtDisplay as qtDisplay
from PDF_Generation.PDF_Elliptical import *

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
        self.window.pushButton_print.clicked.connect(self.printReport)

    def pushButton_generation_clicked(self):
        print(self.sender().text() + "点了")
        self.showElliptical()
        # a_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

        self.display.ResetView()
        # self.display.DisplayShape(a_box, update=True)

    def clear_display(self):
        print(self.sender().text() + "点了")
        self.display.EraseAll()

    # Read input parameters
    def readParameters(self):
        parameters = {}
        Pressure = self.window.lineEdit.text()  # 计算压力 MPa
        temperature = self.window.lineEdit_2.text()  # 设计温度 摄氏度
        Equipment_inner_diameter = self.window.lineEdit_3.text()  # 封头内径
        Depth = self.window.lineEdit_4.text()  # 曲面内深度
        allowable_stress = self.window.lineEdit_5.text()  # 设计温度下的材料的许用应力
        deviation = self.window.lineEdit_6.text()  # 钢板负偏差
        Corrosion_allowance = self.window.lineEdit_7.text()  # 腐蚀裕量
        Processing_thinning = self.window.lineEdit_8.text()  # 加工减薄量
        Welding_factor = self.window.lineEdit_9.text()  # 焊接系数

        if self.is_number(Pressure) \
                and self.is_number(temperature) \
                and self.is_number(Equipment_inner_diameter) \
                and self.is_number(Depth) \
                and self.is_number(allowable_stress) \
                and self.is_number(deviation) \
                and self.is_number(Corrosion_allowance) \
                and self.is_number(Processing_thinning) \
                and self.is_number(Welding_factor):
            print('都是数字')
            parameters = {
                'Pressure': Pressure,
                'temperature': temperature,
                'Equipment_inner_diameter': Equipment_inner_diameter,
                'Depth': Depth,
                'allowable_stress': allowable_stress,
                'deviation': deviation,
                'Corrosion_allowance': Corrosion_allowance,
                'Processing_thinning': Processing_thinning,
                'Welding_factor': Welding_factor
            }
        else:
            print('输入有误')
        return parameters

    def printReport(self):
        parameters = self.readParameters()
        if parameters:
            pdf_generator = PDFGenerator(parameters)
            pdf_generator.genTaskPDF()
        else:
            print('参数为空！')

    def calculateParameters(self):
        parameters = self.readParameters()

        pressure = float(parameters['Pressure'])  # 计算压力 MPa
        temperature = float(parameters['temperature'])  # 设计温度 摄氏度
        Di = float(parameters['Equipment_inner_diameter'])  # 封头内径
        hi = float(parameters['Depth'])  # 曲面内深度
        allowable_stress = float(parameters['allowable_stress'])  # 设计温度下的材料的许用应力
        C1 = float(parameters['deviation'])  # 钢板负偏差
        C2 = float(parameters['Corrosion_allowance'])  # 腐蚀裕量
        C3 = float(parameters['Processing_thinning'])  # 加工减薄量
        E = float(parameters['Welding_factor'])  # 焊接系数

        R = Di / 2
        K = (2 + math.pow((0.5 * Di / hi), 2)) / 6  # 椭圆封头形状系数

        calculate_thickness = round((K * pressure * Di) / (2 * allowable_stress * E - 0.5 * pressure), 2)

        # 封头设计厚度
        design_thickness = round((calculate_thickness + C1 + C2 + C3), 2)

        # 封头名义厚度
        titular_thickness = math.ceil(design_thickness)
        if titular_thickness == 13:
            titular_thickness =14
        a = titular_thickness
        return R,hi,a

    # show Elliptical model
    def showElliptical(self):
        R, hi, a = self.calculateParameters()
        Elli = Elliptical.Elliptical_Head(R, hi, a)
        A = Elli.getElliptical_Head()
        self.display.EraseAll()
        self.display.ResetView()
        self.display.DisplayShape(A.Shape(), update=True)

    #judge a input whether is a number
    def is_number(self, a):
        if a.replace('.', '').isdigit():
            return True
        return False