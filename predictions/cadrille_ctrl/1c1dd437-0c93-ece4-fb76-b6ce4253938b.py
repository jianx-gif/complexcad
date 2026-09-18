import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.workplane(offset=-120/2).moveTo(0,-7).cylinder(120,2).union(w0.sketch().circle(30).reset().face(w0.sketch().segment((-15,-2),(-1,-2)).segment((-3,-14)).segment((2,-15)).segment((4,-2)).segment((15,-2)).segment((15,2)).segment((1,2)).segment((3,14)).segment((-2,15)).segment((-4,2)).segment((-15,2)).close().assemble(),mode='s').finalize().extrude(-30)).union(w0.sketch().circle(20).reset().face(w0.sketch().segment((-12,-2),(1,-12)).segment((12,2)).segment((-1,12)).close().assemble(),mode='s').finalize().extrude(60))
