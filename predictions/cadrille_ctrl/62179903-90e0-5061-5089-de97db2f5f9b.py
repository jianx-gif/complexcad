import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-10,31),(10,31)).arc((0,37),(-10,31)).assemble().finalize().extrude(4).union(w0.sketch().circle(30).circle(5,mode='s').finalize().extrude(30))
