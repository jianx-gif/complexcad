import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-23,-16),(1,-25)).segment((23,16)).segment((-1,25)).close().assemble(),mode='s').push([(41,33)]).circle(34,mode='s').finalize().extrude(60).union(w0.workplane(offset=100/2).cylinder(100,60))