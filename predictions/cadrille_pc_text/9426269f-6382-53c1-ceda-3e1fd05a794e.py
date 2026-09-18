import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
r=w0.sketch().segment((-100,-67),(100,-67)).segment((100,67)).segment((1,67)).segment((1,58)).segment((-1,58)).segment((-1,67)).segment((-100,67)).close().assemble().circle(36,mode='s').finalize().extrude(8).union(w0.workplane(offset=9/2).box(160,12,9))