import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('YZ',origin=(95,0,0))
r=w0.sketch().segment((-10,-39),(10,-39)).segment((10,-38)).arc((0,-38),(-10,-37)).close().assemble().finalize().extrude(117).union(w1.sketch().arc((-85,29),(-68,27),(-51,25)).arc((-28,28),(-6,25)).arc((28,20),(59,7)).arc((68,2),(77,-4)).arc((82,-10),(85,-17)).segment((85,29)).arc((0,82),(-85,29)).assemble().finalize().extrude(-195))