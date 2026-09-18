import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-11,29),(11,29)).arc((0,37),(-11,29)).assemble().finalize().extrude(4).union(w0.sketch().circle(30).circle(5,mode='s').finalize().extrude(30))