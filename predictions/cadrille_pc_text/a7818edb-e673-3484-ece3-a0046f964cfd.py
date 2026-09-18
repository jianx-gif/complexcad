import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-88,-96),(-73,-96)).segment((-73,-100)).segment((73,-100)).segment((73,-96)).segment((88,-96)).segment((88,96)).segment((73,96)).segment((73,100)).segment((-73,100)).segment((-73,96)).segment((-88,96)).close().assemble().rect(134,170,mode='s').finalize().extrude(-30)