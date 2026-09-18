import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('YZ',origin=(-47,0,0))
r=w0.sketch().segment((-100,-20),(100,-20)).segment((100,0)).segment((-100,0)).segment((-100,-2)).arc((-97,-3),(-100,-4)).close().assemble().push([(25.5,-6.5)]).rect(49,7,mode='s').finalize().extrude(125).union(w1.workplane(offset=-30/2).moveTo(37.5,0).box(7,126,30))