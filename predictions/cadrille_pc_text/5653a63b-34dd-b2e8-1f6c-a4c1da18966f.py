import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,72,0))
r=w0.sketch().circle(100).circle(45,mode='s').push([(61,6)]).rect(22,114,mode='s').finalize().extrude(-144)