import cadquery as cq
w0=cq.Workplane('YZ',origin=(-36,0,0))
w1=cq.Workplane('ZX',origin=(0,-32,0))
r=w0.sketch().segment((-26,90),(26,90)).arc((0,95),(-26,90)).assemble().finalize().extrude(-14).union(w0.sketch().push([(0,-74)]).circle(26).circle(24,mode='s').finalize().extrude(122)).union(w1.sketch().push([(0,-44)]).circle(42).circle(41,mode='s').finalize().extrude(65))