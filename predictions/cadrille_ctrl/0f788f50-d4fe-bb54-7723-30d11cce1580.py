import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
w1=cq.Workplane('YZ',origin=(30,0,0))
r=w0.sketch().rect(80,60).reset().face(w0.sketch().segment((-30,-15),(30,-15)).segment((30,15)).segment((-30,15)).segment((-30,10)).arc((-31,7),(-30,4)).close().assemble(),mode='s').finalize().extrude(-8).union(w0.sketch().rect(40,60).circle(20,mode='s').finalize().extrude(-8)).union(w1.workplane(offset=-59/2).moveTo(0,0.5).box(30,7,59))
