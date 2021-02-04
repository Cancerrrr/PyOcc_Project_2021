from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder,BRepPrimAPI_MakeRevol
from OCC.Core.gp import gp_Pnt,gp_Ax1,gp_Ax2,gp_Dir,gp_Vec
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Fuse
from OCC.Core.GC import GC_MakeCircle
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BOPAlgo import BOPAlgo_Splitter
from OCC.Extend.TopologyUtils import TopologyExplorer
import  threading
from OCC.Display.SimpleGui import init_display
#display, start_display, add_menu, add_function_to_menu = init_display()

class TTKaikong(threading.Thread):
    def __init__(self, D_i = 1000, t = 35, l = 2000, R_n = 100, L_pr1 = 50, t_n = 50, t_n2 = 0, t_e = 0, L_pr2 = 0, L_pr3 = 0, Hole_pos = 1000):
        threading.Thread.__init__(self)
        # 圆柱
        self.D_i = D_i  # 壳体内径
        self.R = D_i / 2  # 外壳半径
        self.t = t  # 壳厚度
        self.l = l  # 圆筒长度
        self.r = self.R - self.t  # 壳内径

        # 开孔尺寸
        self.R_n = R_n  # 接管内半径
        self.L_pr1 = L_pr1  # 容器壁外侧接管伸出长度
        self.t_n = t_n  # 接管壁厚度
        self.t_n2 = t_n2  # 变厚度接管较薄部分公称厚度
        self.t_e = t_e  # 补强板厚度
        self.L_pr2 = L_pr2  # 容器壁内侧接管伸出长度
        self.L_pr3 = L_pr3  # 外侧变厚度t的长度

        # 开孔位置
        self.Hole_pos = Hole_pos
        self.new_thing0 = ''

    def run(self) -> None:
        edge = BRepBuilderAPI_MakeEdge(gp_Pnt(self.r, 0, 0), gp_Pnt(0, 0, 0)).Edge()
        # 筒体
        cylinder1 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), self.R, self.l).Shape()
        cylinder2 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), self.r, self.l).Shape()
        new_thing1 = BRepAlgoAPI_Cut(cylinder1, cylinder2).Shape()

        # 布尔剪打孔
        my_cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, self.Hole_pos, 0), gp_Dir(1, 0, 0)), self.R_n + self.t_n,
                                               self.l).Shape()  # 参数按照顺序为孔圆心位置，方向，半径，孔深
        new_thing2 = BRepAlgoAPI_Cut(new_thing1, my_cylinder).Shape()

        # 加管
        cylinder3 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, self.Hole_pos, 0), gp_Dir(1, 0, 0)), self.R_n + self.t_n,
                                             self.r + self.t + self.L_pr1).Shape()
        cylinder4 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, self.Hole_pos, 0), gp_Dir(1, 0, 0)), self.R_n,
                                             self.r + self.t + self.L_pr1).Shape()
        new_thing3 = BRepAlgoAPI_Cut(cylinder3, cylinder4).Shape()
        new_thing = BRepAlgoAPI_Fuse(new_thing2, new_thing3).Shape()

        # 切内部管
        Circle = GC_MakeCircle(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), self.r).Value()
        aEdge = BRepBuilderAPI_MakeEdge(Circle)
        aWire = BRepBuilderAPI_MakeWire(aEdge.Edge())
        AddFace = BRepBuilderAPI_MakeFace(aWire.Wire())

        splitter = BOPAlgo_Splitter()
        splitter.AddArgument(AddFace.Face())
        splitter.AddTool(edge)
        splitter.Perform()

        for shape in TopologyExplorer(splitter.Shape()).faces():
            True
        B = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), self.r, self.l).Shape()
        self.new_thing0 = BRepAlgoAPI_Cut(new_thing, B).Shape()

'''if __name__ == "__main__":
    kaikong = TTKaikong()
    kaikong.start()
    kaikong.join()
    display.DisplayShape(kaikong.new_thing0, update=True)
    start_display()'''