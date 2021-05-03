from OCC.Core.gp import gp_Pnt, gp_OX, gp_Trsf, gp_Vec, gp_DZ, gp_Ax2, gp_Dir, gp_Ax1
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeRevol
from OCC.Core.BOPAlgo import BOPAlgo_Splitter
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.SimpleGui import init_display
import math

display, start_display, add_menu, add_function_to_menu = init_display()


class Elliptical_Head():
    def __init__(self):
        # display, start_display, add_menu, add_function_to_menu = init_display()
        Location = gp_Pnt(0, 0, 0)
        Axis = gp_Dir(0, 0, 1)
        b = math.pi
        R = 500  # 外长径
        r = 300  # 外短径
        l = 300  # 突出的长度
        a = 40  # 壁厚
        CircleAxis = gp_Ax2(Location, Axis)
        aPnt1 = gp_Pnt(0, 0, R)
        aPnt2 = gp_Pnt(r, 0, 0)
        aPnt3 = gp_Pnt(0, 0, -R)
        aPnt4 = gp_Pnt(-l, 0, R)
        aPnt5 = gp_Pnt(-l, 0, -R)
        aPnt6 = gp_Pnt(-l, 0, -R + a)
        aPnt7 = gp_Pnt(0, 0, -R + a)
        aPnt8 = gp_Pnt(r - a, 0, 0)
        aPnt9 = gp_Pnt(0, 0, R - a)
        aPnt10 = gp_Pnt(-l, 0, R - a)

        aArcOfCircle1 = GC_MakeArcOfCircle(aPnt1, aPnt2, aPnt3)  # GC_MakeArcOfEllipse

        aEdge1 = BRepBuilderAPI_MakeEdge(aArcOfCircle1.Value())

        aArcOfCircle2 = GC_MakeArcOfCircle(aPnt7, aPnt8, aPnt9)
        aEdge2 = BRepBuilderAPI_MakeEdge(aArcOfCircle2.Value())
        aSegment1 = GC_MakeSegment(aPnt1, aPnt4)
        aSegment2 = GC_MakeSegment(aPnt4, aPnt10)
        aSegment3 = GC_MakeSegment(aPnt10, aPnt9)
        aSegment4 = GC_MakeSegment(aPnt7, aPnt6)
        aSegment5 = GC_MakeSegment(aPnt6, aPnt5)
        aSegment6 = GC_MakeSegment(aPnt5, aPnt3)
        aSegment7 = GC_MakeSegment(aPnt2, aPnt8)
        aEdge3 = BRepBuilderAPI_MakeEdge(aSegment1.Value())
        aEdge4 = BRepBuilderAPI_MakeEdge(aSegment2.Value())
        aEdge5 = BRepBuilderAPI_MakeEdge(aSegment3.Value())
        aEdge6 = BRepBuilderAPI_MakeEdge(aSegment4.Value())
        aEdge7 = BRepBuilderAPI_MakeEdge(aSegment5.Value())
        aEdge8 = BRepBuilderAPI_MakeEdge(aSegment6.Value())
        aEdge9 = BRepBuilderAPI_MakeEdge(aSegment7.Value())
        aWire1 = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge3.Edge(), aEdge4.Edge(), aEdge5.Edge())
        aWire2 = BRepBuilderAPI_MakeWire(aEdge2.Edge(), aEdge6.Edge(), aEdge7.Edge(), aEdge8.Edge())

        # 合并两条曲线段
        mkWire = BRepBuilderAPI_MakeWire()
        mkWire.Add(aWire1.Wire())
        mkWire.Add(aWire2.Wire())
        myWireProfile = mkWire.Wire()
        # 计算总面积
        myFaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)

        # 切割线
        edge = BRepBuilderAPI_MakeEdge(aPnt2, aPnt8).Edge()
        # 切割函数
        splitter = BOPAlgo_Splitter()
        splitter.AddArgument(myFaceProfile.Face())
        splitter.AddTool(edge)
        splitter.Perform()
        # 显示分割后的面
        for shape in TopologyExplorer(splitter.Shape()).faces():
            #display.DisplayShape(shape, update=True)
        # 旋转
            self.A = BRepPrimAPI_MakeRevol(shape, gp_Ax1(Location, gp_Dir(1, 0, 0)))
    def getElliptical_Head(self):
        return self.A


if __name__ == "__main__":
    Elliptical = Elliptical_Head()
    A = Elliptical.getElliptical_Head()
    display.DisplayShape(A.Shape(), update=True)
    start_display()