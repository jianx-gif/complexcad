import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,34,0))
r=w0.sketch().push([(0,44)]).circle(56).rect(12,102,mode='s').push([(-8,-92)]).circle(8).finalize().extrude(-68)