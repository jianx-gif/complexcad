import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
w1=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-95,-1),(1,-95)).segment((95,1)).segment((-1,95)).close().assemble(),mode='s').finalize().extrude(63).union(w0.sketch().segment((-90,-1),(-86,-1)).arc((0,-86),(86,-1)).segment((90,-1)).segment((90,1)).segment((86,1)).arc((0,86),(-86,1)).segment((-90,1)).close().assemble().finalize().extrude(125)).union(w1.workplane(offset=97/2).cylinder(97,70))