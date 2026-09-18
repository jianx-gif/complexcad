import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.workplane(offset=15/2).moveTo(0,-10).box(198,130,15).union(w0.sketch().segment((-100,-65),(90,-65)).segment((90,65)).segment((-100,65)).segment((-100,-12)).segment((-90,-12)).segment((-90,62)).segment((90,62)).segment((90,-62)).segment((-90,-62)).segment((-90,-18)).segment((-100,-18)).close().assemble().finalize().extrude(35))