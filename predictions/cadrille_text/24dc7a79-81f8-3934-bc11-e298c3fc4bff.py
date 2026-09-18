import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-32))
w1=cq.Workplane('XY',origin=(-87,0,-32))
r=w0.sketch().segment((-87,-28),(-87,28)).arc((-92,0),(-87,-28)).assemble().finalize().extrude(64).union(w1.sketch().push([(0,0.5)]).rect(12,11).push([(0,0)]).circle(3,mode='s').finalize().extrude(64))