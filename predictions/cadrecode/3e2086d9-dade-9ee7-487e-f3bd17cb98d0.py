import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,34,0))
r=w0.sketch().circle(100).push([(49.5,0)]).rect(83,38,mode='s').finalize().extrude(-60).union(w0.workplane(offset=62/2).cylinder(62,72)).union(w1.workplane(offset=-96/2).cylinder(96,98))