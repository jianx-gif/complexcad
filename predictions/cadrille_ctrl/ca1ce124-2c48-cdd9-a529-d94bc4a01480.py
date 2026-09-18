import cadquery as cq
w0=cq.Workplane('YZ',origin=(20,0))
w1=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().segment((-4,7),(11,7)).segment((11,11)).segment((-4,11)).close().assemble().finalize().extrude(-1).union(w0.sketch().segment((-4,7),(11,7)).segment((11,13)).segment((-4,13)).close().assemble().finalize().extrude(-1))
