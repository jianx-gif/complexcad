import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(100).circle(86,mode='s').finalize().extrude(17).union(w0.sketch().circle(83).circle(16,mode='s').finalize().extrude(122)).union(w0.sketch().segment((-72,-3),(72,-3)).arc((0,75),(-72,-3)).assemble().finalize().extrude(150))