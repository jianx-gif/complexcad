import cadquery as cq
w0=cq.Workplane('XY',origin=(-47,0,-47))
r=w0.sketch().segment((28,-58),(47,-58)).segment((47,-51)).arc((38,-54),(28,-51)).close().assemble().finalize().extrude(24).union(w0.workplane(offset=94/2).moveTo(0,1).cylinder(94,3))