import cadquery as cq
w0=cq.Workplane('YZ',origin=(-43,0,0))
w1=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().push([(0,15.5)]).rect(46,35).push([(0,15)]).rect(40,30,mode='s').finalize().extrude(86).union(w1.sketch().push([(0,15)]).rect(44,36).push([(0,14.5)]).rect(40,33,mode='s').finalize().extrude(63))
