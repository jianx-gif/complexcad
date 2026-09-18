import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-70/2).moveTo(0,-1).cylinder(70,2).union(w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(30)).union(w0.sketch().circle(21).reset().face(w0.sketch().segment((-16,-10),(-12,-12)).segment((-10,-7)).segment((-14,-6)).close().assemble(),mode='s').push([(9,0)]).circle(6,mode='s').finalize().extrude(70))