import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
w1=cq.Workplane('YZ',origin=(38,0,0))
r=w0.sketch().push([(0,-1)]).rect(60,38).push([(0,-1.5)]).rect(34,17,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-15,-32),(15,-32)).segment((15,-22)).arc((0,-20),(-15,-11)).close().assemble().reset().face(w0.sketch().arc((-15,19),(0,28),(15,26)).segment((15,32)).segment((-15,32)).close().assemble()).finalize().extrude(8)).union(w0.workplane(offset=8/2).moveTo(0,-25).cylinder(8,8)).union(w1.workplane(offset=42/2).moveTo(0,4).cylinder(42,2))