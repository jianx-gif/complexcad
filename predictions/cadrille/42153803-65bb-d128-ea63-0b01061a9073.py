import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,93))
r=w0.sketch().rect(94,48).reset().face(w0.sketch().segment((-38,-14),(-13,-14)).arc((0,-18),(13,-14)).segment((38,-14)).segment((38,14)).segment((13,14)).arc((0,18),(-13,14)).segment((-38,14)).close().assemble(),mode='s').finalize().extrude(-188).union(w1.sketch().segment((-66,-7),(-48,-7)).segment((-48,-7),(-46,-7)).segment((-46,-1)).segment((-40,-1)).segment((-40,-7)).segment((66,-7)).segment((66,7)).segment((-66,7)).close().assemble().finalize().extrude(-193))