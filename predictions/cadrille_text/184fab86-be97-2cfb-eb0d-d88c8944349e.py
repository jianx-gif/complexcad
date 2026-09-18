import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('XY',origin=(0,0,-47))
r=w0.sketch().segment((29,-58),(33,-58)).segment((33,-57)).close().assemble().finalize().extrude(113).union(w1.workplane(offset=102/2).moveTo(0,9.5).box(100,3,102))