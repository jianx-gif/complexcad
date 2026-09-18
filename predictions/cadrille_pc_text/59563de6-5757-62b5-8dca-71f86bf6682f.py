import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-52))
r=w0.sketch().segment((-56,-5),(-40,-5)).arc((0,-40),(40,-5)).segment((56,-5)).segment((56,5)).segment((40,5)).arc((0,40),(-40,5)).segment((-56,5)).close().assemble().finalize().extrude(200).union(w1.sketch().circle(56).circle(41,mode='s').finalize().extrude(100))