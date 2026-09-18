import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-99,-49),(99,-49)).segment((99,49)).segment((-99,49)).segment((-99,47)).segment((97,47)).segment((97,-47)).segment((-99,-47)).close().assemble().finalize().extrude(200).union(w0.sketch().segment((-73,41),(67,49)).arc((-5,73),(-73,41)).assemble().finalize().extrude(200))