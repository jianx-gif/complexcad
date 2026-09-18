import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().segment((-28,-3),(-20,-3)).arc((-21,0),(-20,3)).segment((-28,3)).close().assemble().reset().face(w0.sketch().segment((20,-3),(28,-3)).segment((28,3)).segment((20,3)).arc((21,0),(20,-3)).assemble()).finalize().extrude(-161).union(w0.sketch().rect(40,20).rect(32,12,mode='s').finalize().extrude(-80))