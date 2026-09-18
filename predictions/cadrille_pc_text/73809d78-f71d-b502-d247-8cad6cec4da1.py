import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,17))
r=w0.sketch().segment((-100,-43),(32,-44)).segment((33,43)).segment((-99,44)).close().assemble().circle(11,mode='s').finalize().extrude(-45).union(w0.sketch().segment((-71,-33),(-19,-33)).segment((-19,25)).segment((23,25)).segment((23,-33)).segment((71,-33)).segment((71,33)).segment((-71,33)).close().assemble().finalize().extrude(11))