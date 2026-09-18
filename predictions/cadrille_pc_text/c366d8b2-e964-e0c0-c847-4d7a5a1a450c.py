import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.sketch().segment((-100,-11),(-57,-23)).arc((20,-2),(96,-34)).segment((100,-31)).segment((100,6)).arc((0,33),(-100,-11)).assemble().finalize().extrude(36)