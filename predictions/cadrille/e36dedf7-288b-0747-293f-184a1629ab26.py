import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
w1=cq.Workplane('XY',origin=(0,0,-32))
r=w0.workplane(offset=6/2).cylinder(6,100).union(w0.sketch().circle(84).circle(78,mode='s').finalize().extrude(54)).union(w1.sketch().circle(83).circle(5,mode='s').finalize().extrude(52))