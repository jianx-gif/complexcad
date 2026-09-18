import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('ZX',origin=(0,91,0))
r=w0.sketch().segment((-100,-40),(-99,-40)).segment((-99,-75)).segment((94,-75)).segment((94,-40)).segment((100,-40)).segment((100,75)).segment((-100,75)).close().assemble().circle(25,mode='s').finalize().extrude(-20).union(w1.sketch().arc((57,-24),(60,0),(57,24)).close().assemble().finalize().extrude(-143))