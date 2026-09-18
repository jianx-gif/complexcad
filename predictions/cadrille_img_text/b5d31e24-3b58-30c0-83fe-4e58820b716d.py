import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('YZ',origin=(26,0,0))
r=w0.sketch().segment((-48,80),(-19,22)).segment((87,-28)).arc((39,23),(-27,34)).segment((48,34)).segment((48,80)).close().assemble().finalize().extrude(-29).union(w0.sketch().arc((-43,77),(-30,49),(-24,20)).segment((55,20)).arc((5,49),(-43,77)).assemble().finalize().extrude(78)).union(w1.sketch().arc((-10,48),(1,29),(5,8)).arc((20,39),(-10,58)).close().assemble().finalize().extrude(-102))