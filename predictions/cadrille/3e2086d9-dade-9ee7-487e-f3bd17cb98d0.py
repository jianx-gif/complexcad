import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,31,0))
r=w0.sketch().circle(100).push([(45,0)]).circle(19,mode='s').finalize().extrude(-63).union(w0.workplane(offset=62/2).cylinder(62,70)).union(w1.sketch().circle(89).push([(45,0)]).circle(19,mode='s').finalize().extrude(-31))