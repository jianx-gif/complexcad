import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
r=w0.sketch().circle(100).push([(49,10)]).circle(37,mode='s').finalize().extrude(-58).union(w0.workplane(offset=42/2).cylinder(42,57)).union(w0.workplane(offset=114/2).cylinder(114,43))