import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-11))
r=w0.workplane(offset=-22/2).cylinder(22,100).union(w0.sketch().circle(82).circle(82,mode='s').finalize().extrude(45))