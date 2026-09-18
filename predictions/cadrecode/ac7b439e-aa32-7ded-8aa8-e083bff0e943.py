import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,39))
w1=cq.Workplane('XY',origin=(0,0,34))
r=w0.workplane(offset=-139/2).box(56,42,139).union(w0.sketch().segment((-43,-1),(-40,-1)).segment((-40,-15)).arc((41,12),(-43,-1)).assemble().finalize().extrude(32)).union(w0.workplane(offset=61/2).box(44,6,61)).union(w1.sketch().segment((-28,-19),(-24,-19)).segment((-24,-21)).segment((24,-21)).segment((24,-19)).segment((28,-19)).segment((28,21)).segment((24,21)).segment((-24,21)).segment((-28,21)).close().assemble().finalize().extrude(-130))