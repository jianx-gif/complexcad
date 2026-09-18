import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().rect(50,100).push([(-10,25)]).circle(14,mode='s').push([(-12,-28)]).circle(13,mode='s').push([(13,-20)]).circle(3,mode='s').finalize().extrude(-200)