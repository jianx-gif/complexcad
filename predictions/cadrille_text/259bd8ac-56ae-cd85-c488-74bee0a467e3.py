import cadquery as cq
w0=cq.Workplane('XY',origin=(-75,-75,-100))
r=w0.sketch().segment((-75,75),(-74,75)).segment((-74,74)).arc((-73,77),(-75,75)).assemble().finalize().extrude(200)