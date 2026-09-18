import cadquery as cq
w0=cq.Workplane('XY',origin=(-58,0,-100))
w1=cq.Workplane('XY',origin=(-58,0,-60))
r=w0.sketch().segment((92,100),(93,98)).segment((93,100)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(58,0)]).circle(10).push([(58.5,0)]).rect(13,10,mode='s').finalize().extrude(150))