import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().arc((29,43),(30,43),(30,42)).arc((31,43),(29,43)).assemble().finalize().extrude(-61).union(w0.sketch().arc((-29,39),(27,-44),(-26,42)).segment((-26,39)).close().assemble().push([(0,1)]).circle(31,mode='s').finalize().extrude(-8))
