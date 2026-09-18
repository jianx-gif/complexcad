import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,58)).segment((96,58)).segment((96,62)).segment((-96,62)).segment((-96,58)).segment((-100,58)).close().assemble().circle(10,mode='s').finalize().extrude(75)