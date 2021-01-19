#!/usr/bin/env python
# coding: utf-8

# In[1]:


from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_DZ, gp_OX, gp_Trsf, gp_Vec, gp_Dir, gp_Circ, gp_Ax1
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeRevol,     BRepPrimAPI_MakeBox
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet


# In[2]:

class Cylinder():
    def __init__(self, R = 500, t = 30, L = 100):
        # 模型定义
        self.R = R
        self.t = t
        self.L = L
        P1 = gp_Pnt(-self.R, 0, 0)
        P2 = gp_Pnt(0, self.R, 0)
        P3 = gp_Pnt(self.R, 0, 0)
        P4 = gp_Pnt(self.R - self.t, 0, 0)
        P5 = gp_Pnt(0, self.R - self.t, 0)
        P6 = gp_Pnt(self.t - self.R, 0, 0)
        P7 = gp_Pnt(0, self.t - self.R, 0)
        P8 = gp_Pnt(0, -self.R, 0)

        # In[3]:

        Circle1 = GC_MakeArcOfCircle(P1, P2, P3)
        Circle2 = GC_MakeArcOfCircle(P4, P5, P6)
        Circle3 = GC_MakeArcOfCircle(P4, P7, P6)
        Circle4 = GC_MakeArcOfCircle(P3, P8, P1)


        # In[4]:
        ##定义拓扑信息
        aEdge3 = BRepBuilderAPI_MakeEdge(Circle1.Value())
        aEdge4 = BRepBuilderAPI_MakeEdge(Circle2.Value())
        aEdge5 = BRepBuilderAPI_MakeEdge(Circle3.Value())
        aEdge6 = BRepBuilderAPI_MakeEdge(Circle4.Value())

        # In[5]:

        W1 = BRepBuilderAPI_MakeWire(aEdge3.Edge(), aEdge6.Edge())
        W2 = BRepBuilderAPI_MakeWire(aEdge4.Edge(), aEdge5.Edge())
        S1 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(W1.Wire()).Face(), gp_Vec(0., 0, self.L))
        S2 = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(W2.Wire()).Face(), gp_Vec(0., 0, self.L))

        # In[6]:

        my_cylinder = S2.Shape()
        my_box = S1.Shape()
        self.new_thing1 = BRepAlgoAPI_Cut(my_box, my_cylinder).Shape()

        # In[7]:







'''if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    C = Cylinder(500,100,1000)

    #display.DisplayShape(W2.Shape(), update=True)
    #display.DisplayShape(S1.Shape(), update=True)
    #display.DisplayShape(S2.Shape(), update=True)
    display.DisplayShape(C.new_thing1, update=True)
    start_display()'''

# In[ ]:




