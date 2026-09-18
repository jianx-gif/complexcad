import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().rect(50,100).push([(-10,33)]).circle(13,mode='s').push([(-6,-25)]).circle(12,mode='s').push([(0,0)]).circle(9,mode='s').finalize().extrude(-200)