import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-47,0,0))
r=w0.sketch().segment((-89,-59),(89,-59)).segment((89,15)).segment((-89,-58)).close().assemble().reset().face(w0.sketch().segment((-89,-15),(89,58)).segment((89,59)).segment((-89,59)).close().assemble()).finalize().extrude(200).union(w1.workplane(offset=101/2).moveTo(0,-53).cylinder(101,11))