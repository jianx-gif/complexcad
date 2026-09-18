import cadquery as cq
w0=cq.Workplane('YZ',origin=(49,0,0))
r=w0.sketch().segment((-100,6),(-99,-7)).segment((100,-6)).segment((100,7)).close().assemble().reset().face(w0.sketch().segment((-32,-4),(-29,-4)).arc((-14,-6),(-28,0)).segment((-32,0)).close().assemble(),mode='s').push([(18,-3)]).circle(13,mode='s').finalize().extrude(-99)