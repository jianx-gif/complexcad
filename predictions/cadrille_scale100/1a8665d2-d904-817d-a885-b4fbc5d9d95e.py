import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((37,-1),(45,0)).arc((-45,3),(44,-9)).segment((39,-10)).close().assemble().reset().face(w0.sketch().segment((-35,-2),(-17,-10)).arc((-11,-11),(-7,-15)).segment((11,-22)).segment((21,8)).segment((-19,22)).close().assemble(),mode='s').finalize().extrude(20)