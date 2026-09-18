import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().circle(100).circle(80,mode='s').finalize().extrude(-99).union(w1.sketch().circle(90).push([(-27,18)]).circle(13,mode='s').push([(27,-17)]).circle(7,mode='s').finalize().extrude(10))