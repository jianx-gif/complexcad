import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-7))
r=w0.workplane(offset=-10/2).moveTo(-1,0).box(168,118,10).union(w0.sketch().segment((-100,-58),(88,-58)).segment((88,-36)).segment((100,-36)).segment((100,36)).segment((88,36)).segment((88,58)).segment((-100,58)).close().assemble().rect(180,98,mode='s').finalize().extrude(24))