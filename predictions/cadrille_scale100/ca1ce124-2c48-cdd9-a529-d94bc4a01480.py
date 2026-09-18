import cadquery as cq
w0=cq.Workplane('YZ',origin=(20,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-4,7),(11,7)).segment((11,11)).segment((-4,11)).close().assemble().finalize().extrude(-1).union(w0.sketch().segment((-4,7),(13,7)).segment((13,11)).segment((-4,11)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((-4,78),(30,78)).segment((30,80)).segment((-4,80)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((-4,7),(30,0)).segment((31,4)).segment((-3,11)).close().assemble().finalize().extrude(12))