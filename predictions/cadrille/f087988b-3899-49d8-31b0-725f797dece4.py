import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.workplane(offset=24/2).cylinder(24,100).union(w0.workplane(offset=44/2).cylinder(44,38))