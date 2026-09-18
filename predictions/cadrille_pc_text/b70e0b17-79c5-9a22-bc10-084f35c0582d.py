import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('XY',origin=(0,0,-5))
r=w0.sketch().segment((-79,-13),(-76,-9)).segment((-79,-9)).close().assemble().finalize().extrude(21).union(w0.sketch().arc((-77,-9),(1,6),(73,-32)).segment((100,-17)).arc((10,37),(-77,-9)).assemble().finalize().extrude(52)).union(w1.workplane(offset=-21/2).moveTo(-68,-24.5).box(64,25,21))