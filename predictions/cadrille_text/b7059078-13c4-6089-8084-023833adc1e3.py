import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-100,-67))
r=w0.sketch().segment((26,-62),(26,62)).arc((1,0),(26,-62)).assemble().finalize().extrude(133).union(w0.sketch().segment((-57,90),(57,90)).arc((0,100),(-57,90)).assemble().finalize().extrude(133))