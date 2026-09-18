import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,16))
r=w0.sketch().push([(89,-2)]).circle(5).push([(89.5,-2)]).rect(7,4,mode='s').finalize().extrude(-51).union(w0.sketch().segment((-100,-36),(89,-36)).arc((91,-34),(93,-31)).segment((93,36)).segment((-100,36)).close().assemble().finalize().extrude(19))