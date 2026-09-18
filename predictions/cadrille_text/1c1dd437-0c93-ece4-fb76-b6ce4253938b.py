import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-71))
r=w0.sketch().segment((91,-89),(100,-89)).segment((100,-87)).close().assemble().finalize().extrude(142).union(w0.workplane(offset=142/2).moveTo(54,-1).cylinder(142,26))