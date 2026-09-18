import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.workplane(offset=16/2).box(180,150,16).union(w0.sketch().segment((-100,-65),(-90,-65)).segment((-90,65)).segment((90,65)).segment((90,-65)).segment((100,-65)).segment((100,65)).segment((-100,65)).close().assemble().finalize().extrude(36))