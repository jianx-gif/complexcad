import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-38,-53),(-28,-19)).arc((-35,-36),(-38,-53)).assemble().reset().face(w0.sketch().segment((-15,-10),(71,-35)).arc((35,-1),(-15,-10)).assemble()).finalize().extrude(-200).union(w0.sketch().segment((-69,-12),(15,-12)).segment((-15,86)).segment((15,94)).segment((-69,94)).close().assemble().finalize().extrude(-183))