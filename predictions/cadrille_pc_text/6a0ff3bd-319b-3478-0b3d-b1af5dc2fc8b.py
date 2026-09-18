import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-98))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-61,-5),(-42,-2)).segment((-39,-26)).segment((44,-29)).segment((44,-28)).arc((39,-15),(49,-5)).segment((41,29)).segment((-42,26)).segment((-42,25)).segment((-61,4)).close().assemble().finalize().extrude(198).union(w1.sketch().arc((-61,-34),(0,-36),(61,-16)).segment((61,34)).arc((0,36),(-61,34)).segment((-61,26)).arc((52,0),(-61,-26)).close().assemble().finalize().extrude(100))