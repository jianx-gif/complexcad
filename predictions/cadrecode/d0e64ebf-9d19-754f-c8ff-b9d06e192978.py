import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,75))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-42,11),(-37,6)).arc((-25,-28),(11,-36)).segment((16,-41)).segment((42,-11)).segment((37,-6)).arc((25,28),(-11,36)).segment((-16,41)).close().assemble(),mode='s').push([(37,72)]).circle(11,mode='s').finalize().extrude(-150)