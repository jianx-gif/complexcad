import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-20/2).moveTo(19.5,0).box(47,2,20).union(w0.sketch().segment((-40,-25),(40,-25)).segment((40,25)).segment((-40,25)).segment((-40,24)).arc((-38,23),(-40,22)).close().assemble().circle(6,mode='s').finalize().extrude(25))