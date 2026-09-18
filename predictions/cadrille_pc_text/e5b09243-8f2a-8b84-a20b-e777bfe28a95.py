import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
w1=cq.Workplane('YZ',origin=(-79,0,0))
r=w0.sketch().segment((-100,18),(-36,-35)).segment((26,20)).segment((100,20)).arc((67,28),(36,35)).segment((36,23)).segment((-97,23)).close().assemble().finalize().extrude(149).union(w1.workplane(offset=104/2).moveTo(19,0).cylinder(104,3))