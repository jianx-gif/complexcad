import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().segment((-69,-54),(-57,-54)).segment((-57,-24)).arc((-41,-1),(-57,24)).segment((-57,54)).segment((-69,54)).segment((-69,24)).arc((-85,-1),(-69,-24)).close().assemble().finalize().extrude(86).union(w0.workplane(offset=120/2).moveTo(40,16).cylinder(120,40)).union(w1.sketch().arc((-97,22),(85,-50),(-58,82)).arc((-79,53),(-97,22)).assemble().finalize().extrude(-64))