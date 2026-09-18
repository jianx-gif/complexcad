import cadquery as cq
w0=cq.Workplane('YZ',origin=(78,0,0))
r=w0.workplane(offset=-156/2).moveTo(37.5,0).box(7,126,156).union(w0.sketch().segment((-100,-20),(100,-20)).segment((100,0)).segment((50,0)).segment((50,-10)).segment((3,-10)).segment((3,0)).segment((-100,0)).close().assemble().finalize().extrude(-126))