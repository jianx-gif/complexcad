import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,98))
r=w0.sketch().segment((-30,-20),(20,-20)).segment((20,-6)).segment((30,-8)).segment((30,8)).segment((20,6)).segment((20,20)).segment((-30,20)).close().assemble().finalize().extrude(-200).union(w1.sketch().arc((-30,-19),(0,-31),(30,-19)).close().assemble().finalize().extrude(-196))