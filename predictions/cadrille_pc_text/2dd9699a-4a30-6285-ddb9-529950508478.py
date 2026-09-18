import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,45,0))
r=w0.sketch().push([(-7.5,0)]).rect(19,192).push([(-7,-77)]).circle(2,mode='s').push([(-7,77)]).circle(6,mode='s').finalize().extrude(-145).union(w0.workplane(offset=55/2).moveTo(9.5,0).box(15,14,55))