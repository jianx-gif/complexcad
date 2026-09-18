import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-100,-68),(-94,-68)).segment((-94,-75)).segment((94,-75)).segment((94,-68)).segment((100,-68)).segment((100,68)).segment((94,68)).segment((94,75)).segment((-94,75)).segment((-94,68)).segment((-100,68)).close().assemble().circle(25,mode='s').finalize().extrude(-20)