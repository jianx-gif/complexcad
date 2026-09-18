import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,11))
r=w0.sketch().segment((-100,-53),(60,-53)).segment((60,27)).segment((100,27)).segment((100,53)).segment((57,53)).segment((-100,26)).close().assemble().finalize().extrude(-22)