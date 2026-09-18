import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('YZ',origin=(-42,0,0))
r=w0.sketch().segment((-30,-40),(-23,-40)).arc((-18,-52),(-10,-60)).segment((10,-60)).segment((30,-40)).segment((30,0)).segment((-30,0)).close().assemble().finalize().extrude(-189).union(w0.sketch().arc((-28,36),(27,-46),(-13,45)).arc((-19,38),(-28,36)).assemble().finalize().extrude(-45)).union(w1.workplane(offset=102/2).moveTo(74,0).cylinder(102,26))