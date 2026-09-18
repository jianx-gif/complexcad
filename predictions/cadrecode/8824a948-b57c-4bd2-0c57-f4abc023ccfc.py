import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().circle(67).push([(-26,-16)]).circle(32,mode='s').push([(-12,55)]).circle(6,mode='s').push([(0,0)]).circle(16,mode='s').finalize().extrude(-60).union(w0.sketch().circle(100).push([(-73,1)]).circle(12,mode='s').push([(-12,0)]).circle(10,mode='s').finalize().extrude(-27))