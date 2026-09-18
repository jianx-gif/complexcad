import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
w1=cq.Workplane('XY',origin=(0,0,-67))
r=w0.sketch().segment((-47,100),(-46,98)).segment((-46,100)).close().assemble().finalize().extrude(100).union(w1.workplane(offset=134/2).moveTo(0,-10).box(4,4,134))