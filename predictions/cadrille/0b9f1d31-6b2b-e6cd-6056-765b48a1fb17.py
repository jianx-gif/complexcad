import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-77,33),(-11,-83)).segment((77,-33)).segment((10,83)).close().assemble().reset().face(w0.sketch().segment((-44,4),(-16,-34)).segment((44,10)).segment((16,48)).close().assemble(),mode='s').finalize().extrude(200)