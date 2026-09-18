import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-80,1),(-47,-12)).arc((-18,-47),(26,-39)).segment((59,-52)).segment((80,-1)).segment((47,12)).arc((18,47),(-26,39)).segment((-59,52)).close().assemble(),mode='s').finalize().extrude(-25)