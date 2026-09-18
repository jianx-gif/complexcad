import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-88))
w1=cq.Workplane('XY',origin=(0,0,-81))
r=w0.sketch().circle(69).circle(14,mode='s').finalize().extrude(-12).union(w0.sketch().segment((-54,-14),(-50,-14)).arc((-6,-47),(40,-14)).segment((44,-14)).segment((44,-3)).segment((40,-3)).arc((-6,30),(-50,-3)).segment((-54,-3)).close().assemble().push([(-6,-1)]).circle(40,mode='s').finalize().extrude(188)).union(w1.sketch().arc((-41,15),(39,-22),(-37,23)).arc((-34,17),(-41,15)).assemble().finalize().extrude(163))