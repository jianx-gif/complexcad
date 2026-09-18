import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().segment((-40,-25),(40,-25)).segment((40,25)).segment((-40,25)).segment((-40,24)).arc((-38,23),(-40,22)).close().assemble().circle(4,mode='s').finalize().extrude(-30).union(w0.sketch().rect(80,50).circle(4,mode='s').finalize().extrude(-30))
