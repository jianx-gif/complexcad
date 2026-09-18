import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().segment((97,100),(98,99)).segment((99,100)).close().assemble().finalize().extrude(-67).union(w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((24,-55),(26,-58)).assemble().finalize().extrude(-45)).union(w0.workplane(offset=73/2).moveTo(-1,0).cylinder(73,3))