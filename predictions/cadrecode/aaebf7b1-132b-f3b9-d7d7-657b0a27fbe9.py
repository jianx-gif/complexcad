import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
w1=cq.Workplane('ZX',origin=(0,-68,0))
r=w0.sketch().segment((-95,-95),(-31,-95)).arc((0,-100),(31,-95)).segment((95,-95)).segment((95,-31)).arc((100,0),(95,31)).segment((95,95)).segment((31,95)).arc((0,100),(-31,95)).segment((-95,95)).segment((-95,31)).arc((-100,0),(-95,-31)).close().assemble().finalize().extrude(-13).union(w0.workplane(offset=115/2).cylinder(115,95)).union(w1.sketch().push([(4,0)]).circle(63).push([(54,-16)]).circle(14,mode='s').finalize().extrude(162))