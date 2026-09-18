import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((28,-50),(28,-42)).arc((27,-46),(28,-50)).assemble().finalize().extrude(99).union(w0.sketch().push([(27,-46)]).circle(10).push([(27,-45.5)]).rect(16,13,mode='s').finalize().extrude(99)).union(w0.sketch().push([(27,-46)]).circle(10).circle(9,mode='s').finalize().extrude(100))