import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-28))
r=w0.sketch().rect(200,200).circle(80,mode='s').finalize().extrude(12).union(w0.sketch().circle(52).circle(49,mode='s').finalize().extrude(56)).union(w0.workplane(offset=56/2).cylinder(56,23))