import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((-100,-39),(-99,-39)).segment((-99,-75)).segment((94,-75)).segment((94,-69)).segment((100,-70)).segment((100,70)).segment((94,70)).segment((94,75)).segment((-99,75)).segment((-99,69)).segment((-100,69)).close().assemble().push([(-1,0)]).circle(24,mode='s').finalize().extrude(20)