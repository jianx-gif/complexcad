import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,7))
r=w0.sketch().segment((-97,-27),(-97,-10)).segment((-88,-10)).segment((-88,-37)).segment((-92,-37)).arc((96,29),(-97,-27)).assemble().circle(32,mode='s').push([(13,-94)]).circle(2,mode='s').finalize().extrude(-25).union(w0.sketch().arc((48,-10),(50,0),(48,10)).close().assemble().finalize().extrude(10))