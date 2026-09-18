import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-25,-4),(25,-4)).arc((0,9),(-25,-4)).assemble().push([(12,2)]).circle(5,mode='s').finalize().extrude(-200)