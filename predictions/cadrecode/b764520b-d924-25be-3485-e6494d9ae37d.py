import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(-37,0,0))
r=w0.sketch().push([(-56,0)]).circle(38).circle(33,mode='s').finalize().extrude(-200).union(w1.sketch().push([(0,0)]).circle(25).circle(20,mode='s').finalize().extrude(131))