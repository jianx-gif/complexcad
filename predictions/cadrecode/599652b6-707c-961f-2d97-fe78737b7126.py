import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-70,-7),(-37,-7)).arc((0,-38),(37,-7)).segment((70,-7)).segment((70,7)).segment((37,7)).arc((0,38),(-37,7)).segment((-70,7)).close().assemble(),mode='s').push([(0,-64)]).circle(9,mode='s').push([(0,64)]).rect(70,10,mode='s').finalize().extrude(20)