import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(38).rect(20,10,mode='s').finalize().extrude(-90).union(w0.sketch().circle(25).reset().face(w0.sketch().segment((-23,-11),(17,-19)).segment((23,11)).segment((-17,19)).close().assemble(),mode='s').finalize().extrude(110))