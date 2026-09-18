import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
w1=cq.Workplane('XY',origin=(0,0,43))
r=w0.sketch().segment((-44,-83),(-30,-87)).segment((44,100)).arc((3,12),(-44,-83)).assemble().finalize().extrude(-101).union(w0.sketch().segment((-19,-68),(-17,-68)).segment((44,66)).segment((42,67)).close().assemble().finalize().extrude(29)).union(w1.sketch().arc((56,82),(58,77),(59,71)).arc((66,79),(56,82)).assemble().finalize().extrude(1))