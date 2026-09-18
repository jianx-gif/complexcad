import cadquery as cq
w0=cq.Workplane('YZ',origin=(79,0,0))
r=w0.sketch().segment((-60,-6),(40,-6)).segment((40,7)).segment((-58,7)).arc((-59,5),(-60,7)).close().assemble().finalize().extrude(-179).union(w0.workplane(offset=21/2).moveTo(29,0).cylinder(21,30))