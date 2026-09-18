import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-27))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((35,-53),(56,-53)).segment((56,-43)).arc((84,-1),(56,42)).segment((56,53)).segment((35,53)).segment((35,42)).arc((5,-1),(35,-43)).close().assemble(),mode='s').finalize().extrude(48).union(w0.sketch().circle(97).circle(45,mode='s').finalize().extrude(54))