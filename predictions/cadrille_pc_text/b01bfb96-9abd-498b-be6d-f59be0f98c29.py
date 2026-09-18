import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-68))
w1=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().circle(100).circle(90,mode='s').finalize().extrude(136).union(w1.sketch().push([(0,-21)]).circle(51).circle(13,mode='s').finalize().extrude(130))