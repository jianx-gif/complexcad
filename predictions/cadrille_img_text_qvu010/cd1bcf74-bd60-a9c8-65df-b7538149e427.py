import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,44,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-99,94),(25,29),(99,-94)).arc((55,49),(-99,94)).assemble().finalize().extrude(-34).union(w1.sketch().arc((-9,-96),(1,-80),(13,-66)).arc((1,-79),(-9,-96)).assemble().finalize().extrude(-174))