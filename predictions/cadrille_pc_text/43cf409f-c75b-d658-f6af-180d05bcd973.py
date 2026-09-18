import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-70))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(140).union(w0.sketch().circle(82).circle(81,mode='s').finalize().extrude(147))