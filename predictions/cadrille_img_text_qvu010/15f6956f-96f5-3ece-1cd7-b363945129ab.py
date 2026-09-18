import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-70))
r=w0.sketch().segment((-98,-6),(98,-6)).segment((98,6)).segment((58,6)).arc((-2,-5),(-62,6)).segment((-98,6)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-58,60),(-52,49),(-47,38)).arc((-11,33),(17,10)).arc((37,19),(58,24)).arc((2,89),(-58,60)).assemble().finalize().extrude(142))