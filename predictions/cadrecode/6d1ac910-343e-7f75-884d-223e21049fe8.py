import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-100,70),(-89,-68)).segment((100,-68)).segment((97,70)).close().assemble().reset().face(w0.sketch().segment((-41,38),(-27,12)).segment((41,45)).segment((27,71)).close().assemble(),mode='s').push([(0,1)]).circle(3,mode='s').push([(48,-65)]).circle(2,mode='s').finalize().extrude(-8)