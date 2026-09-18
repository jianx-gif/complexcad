import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,36))
r=w0.sketch().segment((-48,11),(-48,24)).arc((-49,17),(-48,11)).assemble().reset().face(w0.sketch().arc((24,-58),(49,-17),(24,24)).close().assemble()).finalize().extrude(-93).union(w0.workplane(offset=-70/2).moveTo(0,17).cylinder(70,3))