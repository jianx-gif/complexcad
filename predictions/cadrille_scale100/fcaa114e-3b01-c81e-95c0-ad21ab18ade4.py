import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,70))
r=w0.sketch().segment((-44,-6),(-41,-6)).arc((0,-42),(41,-6)).segment((44,-6)).segment((44,6)).segment((41,6)).arc((0,42),(-41,6)).segment((-44,6)).close().assemble().push([(0,1)]).circle(39,mode='s').finalize().extrude(-70).union(w0.sketch().circle(45).circle(42,mode='s').finalize().extrude(-11))