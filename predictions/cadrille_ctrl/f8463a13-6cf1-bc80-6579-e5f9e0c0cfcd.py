import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((14,-27),(15,-26),(16,-25)).segment((14,-25)).close().assemble().finalize().extrude(-60).union(w0.sketch().circle(30).reset().face(w0.sketch().segment((-25,-10),(15,-25)).segment((25,10)).segment((-15,25)).close().assemble(),mode='s').finalize().extrude(60)).union(w0.workplane(offset=60/2).cylinder(60,17))
