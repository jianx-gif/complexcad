import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
r=w0.workplane(offset=-50/2).cylinder(50,10).union(w0.sketch().arc((-38,13),(36,-17),(-37,16)).segment((-37,13)).close().assemble().finalize().extrude(-10))
