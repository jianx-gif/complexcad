import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-78,-15),(73,-15)).segment((73,15)).segment((-78,15)).segment((-78,1)).arc((-80,-5),(-78,-11)).close().assemble().push([(1,0)]).circle(4,mode='s').finalize().extrude(-42).union(w0.workplane(offset=6/2).moveTo(1,0).cylinder(6,10)).union(w1.sketch().segment((-50,-15),(48,-15)).arc((48,-14),(50,-12)).segment((50,5)).segment((-50,5)).close().assemble().push([(0,-5)]).rect(6,14,mode='s').finalize().extrude(-200))