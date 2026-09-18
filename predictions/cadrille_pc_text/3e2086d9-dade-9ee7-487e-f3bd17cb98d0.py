import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,26,0))
w1=cq.Workplane('ZX',origin=(0,35,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-89).union(w0.workplane(offset=36/2).cylinder(36,62)).union(w1.sketch().circle(76).push([(46,-1)]).circle(20,mode='s').finalize().extrude(-50))