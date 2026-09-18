import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,16))
w1=cq.Workplane('XY',origin=(0,0,-35))
r=w0.sketch().segment((-100,-36),(89,-36)).arc((91,-34),(93,-31)).segment((93,36)).segment((-100,36)).close().assemble().finalize().extrude(19).union(w1.sketch().push([(89,-2)]).circle(11).push([(89,-1.5)]).rect(8,7,mode='s').finalize().extrude(50))