import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(38).rect(20,10,mode='s').finalize().extrude(87).union(w0.sketch().circle(25).reset().face(w0.sketch().segment((-24,-3),(17,-23)).segment((24,-8)).segment((16,-4)).arc((11,15),(-10,13)).segment((-17,16)).close().assemble(),mode='s').finalize().extrude(200))