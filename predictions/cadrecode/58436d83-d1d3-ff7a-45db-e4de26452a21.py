import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
w1=cq.Workplane('ZX',origin=(0,-73,0))
r=w0.sketch().rect(160,200).push([(-18,-33)]).circle(5,mode='s').push([(38,10)]).circle(5,mode='s').finalize().extrude(16).union(w0.workplane(offset=26/2).cylinder(26,30)).union(w1.workplane(offset=173/2).moveTo(-11,-69).box(10,10,173))