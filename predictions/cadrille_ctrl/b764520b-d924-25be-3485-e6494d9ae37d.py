import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(25,0,0))
r=w0.sketch().push([(0,0)]).circle(15).circle(13,mode='s').finalize().extrude(80).union(w1.sketch().push([(0,40)]).circle(10).circle(8,mode='s').finalize().extrude(35))
