import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().rect(150,20).push([(-65,2)]).circle(4,mode='s').push([(0,0)]).circle(14,mode='s').push([(42,2)]).circle(3,mode='s').finalize().extrude(-200)