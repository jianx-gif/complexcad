import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,34))
r=w0.sketch().segment((4,-49),(4,49)).arc((-49,0),(4,-49)).assemble().finalize().extrude(-74).union(w0.sketch().circle(100).circle(10,mode='s').finalize().extrude(-65))