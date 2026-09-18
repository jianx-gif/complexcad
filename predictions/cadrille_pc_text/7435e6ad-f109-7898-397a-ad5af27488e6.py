import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-5))
w1=cq.Workplane('ZX',origin=(0,66,0))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(-14).union(w1.sketch().push([(8,0)]).rect(26,200).push([(-8,10)]).circle(2,mode='s').push([(-11,35)]).circle(3,mode='s').push([(8,0)]).circle(3,mode='s').finalize().extrude(-133))