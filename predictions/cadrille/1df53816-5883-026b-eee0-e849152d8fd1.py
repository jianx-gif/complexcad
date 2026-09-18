import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-93,-62),(-91,-63)).arc((-68,-57),(-46,-64)).segment((-12,-64)).segment((-12,-55)).segment((93,-64)).segment((2,100)).segment((-93,-56)).close().assemble().finalize().extrude(-24).union(w0.sketch().push([(0,-64)]).circle(36).circle(9,mode='s').finalize().extrude(20))