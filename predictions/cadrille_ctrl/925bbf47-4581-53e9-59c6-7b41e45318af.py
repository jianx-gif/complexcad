import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-1,-61),(2,-67)).segment((3,-67)).segment((0,-60)).arc((-1,-61),(-1,-61)).assemble().finalize().extrude(-2).union(w0.sketch().rect(80,60).push([(-25,-12)]).circle(1,mode='s').push([(25,15)]).circle(3,mode='s').finalize().extrude(5)).union(w0.workplane(offset=8/2).cylinder(8,19))
