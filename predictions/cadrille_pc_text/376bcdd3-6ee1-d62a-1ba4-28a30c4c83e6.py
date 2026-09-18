import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,6,0))
r=w0.sketch().segment((-100,-28),(-94,-28)).arc((0,-100),(94,-28)).segment((100,-28)).segment((100,28)).segment((94,28)).arc((0,100),(-94,28)).segment((-100,28)).close().assemble().circle(76,mode='s').finalize().extrude(-13)