import cadquery as cq
w0=cq.Workplane('YZ',origin=(57,0,0))
w1=cq.Workplane('XY',origin=(0,0,1))
r=w0.sketch().segment((-63,-11),(-57,-11)).segment((-43,11)).segment((-51,11)).close().assemble().finalize().extrude(-115).union(w1.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((-100,62)).segment((-100,25)).arc((-26,-10),(-100,-45)).close().assemble().push([(96,1)]).circle(4,mode='s').finalize().extrude(-12))