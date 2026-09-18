import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(56).circle(54,mode='s').finalize().extrude(-25).union(w0.sketch().circle(76).reset().face(w0.sketch().segment((-74,-18),(-65,-31)).segment((-61,-28)).arc((21,-63),(65,14)).segment((74,18)).segment((65,31)).segment((61,28)).arc((-21,63),(-65,-14)).close().assemble(),mode='s').finalize().extrude(175))