import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,28,0))
w1=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().segment((-49,-50),(-49,-39)).arc((-58,0),(-49,39)).segment((-49,50)).arc((-73,0),(-49,-50)).assemble().finalize().extrude(-57).union(w0.sketch().segment((-100,-11),(-94,-11)).arc((0,-75),(94,-11)).segment((100,-11)).segment((100,11)).segment((94,11)).arc((0,75),(-94,11)).segment((-100,11)).close().assemble().finalize().extrude(-57)).union(w1.sketch().circle(90).push([(27,31)]).circle(47,mode='s').finalize().extrude(-60))