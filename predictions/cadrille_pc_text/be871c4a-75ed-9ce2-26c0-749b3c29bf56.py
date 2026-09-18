import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-88,-80),(-84,-80)).segment((-84,-100)).segment((86,-100)).segment((86,-80)).segment((88,-80)).segment((88,-50)).segment((-37,-50)).segment((-37,100)).segment((-84,100)).segment((-84,80)).segment((-88,80)).close().assemble().finalize().extrude(-20)