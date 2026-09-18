import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().rect(20,200).push([(-2,-85)]).circle(7,mode='s').push([(4,13)]).circle(3,mode='s').finalize().extrude(-100)