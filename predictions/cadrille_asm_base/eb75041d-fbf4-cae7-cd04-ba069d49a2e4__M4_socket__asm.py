import cadquery as cq
w0=cq.Workplane('YZ',origin=(-90,0,0))
w1=cq.Workplane('XY',origin=(0,0,-87))
r=w0.sketch().segment((-30,-72),(17,-87)).segment((17,-13)).segment((10,-13)).segment((10,13)).segment((17,13)).segment((17,87)).close().assemble().finalize().extrude(180).union(w1.sketch().arc((-100,19),(0,-11),(100,19)).close().assemble().finalize().extrude(174))