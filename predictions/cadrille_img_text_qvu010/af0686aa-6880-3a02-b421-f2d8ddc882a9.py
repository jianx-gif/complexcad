import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,46))
r=w0.sketch().circle(100).circle(73,mode='s').finalize().extrude(43).union(w1.sketch().arc((-85,19),(-29,-11),(-49,-75)).arc((82,20),(-85,19)).assemble().finalize().extrude(-113))