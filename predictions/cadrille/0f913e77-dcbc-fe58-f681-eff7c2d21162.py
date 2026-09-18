import cadquery as cq
w0=cq.Workplane('YZ',origin=(78,0,0))
r=w0.workplane(offset=-156/2).moveTo(37.5,0).box(7,126,156).union(w0.sketch().segment((-100,-20),(100,-20)).segment((100,0)).segment((-100,0)).segment((-100,-16)).arc((-98,-17),(-100,-18)).close().assemble().push([(26,-7)]).circle(23,mode='s').finalize().extrude(-126))