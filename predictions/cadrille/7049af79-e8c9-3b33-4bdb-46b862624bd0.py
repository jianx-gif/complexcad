import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().rect(150,12).push([(-6,2)]).circle(3,mode='s').finalize().extrude(200)