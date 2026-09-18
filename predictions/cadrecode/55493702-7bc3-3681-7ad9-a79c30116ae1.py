import cadquery as cq
w0=cq.Workplane('YZ',origin=(-8,0,0))
w1=cq.Workplane('YZ',origin=(-5,0,0))
r=w0.workplane(offset=-92/2).moveTo(0,2.5).box(40,17,92).union(w0.sketch().push([(0,2.5)]).rect(66,17).push([(0,2)]).circle(13,mode='s').finalize().extrude(106)).union(w1.workplane(offset=100/2).moveTo(0,-2.5).box(60,23,100))