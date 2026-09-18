import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((12,-39),(13,-36),(15,-38)).arc((1,39),(12,-39)).assemble().finalize().extrude(50).union(w0.sketch().segment((-28,-13),(-17,-13)).arc((-14,-14),(-11,-13)).segment((15,-13)).segment((15,12)).segment((-28,12)).close().assemble().finalize().extrude(50)).union(w0.sketch().push([(0,1)]).circle(40).reset().face(w0.sketch().segment((-28,-10),(27,-28)).segment((35,-3)).segment((-20,15)).close().assemble(),mode='s').finalize().extrude(60))
