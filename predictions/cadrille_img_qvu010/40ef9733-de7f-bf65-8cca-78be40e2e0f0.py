import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-3,-90),(3,-90)).segment((3,-24)).arc((24,0),(3,24)).segment((3,90)).segment((-3,90)).segment((-3,24)).arc((-24,0),(-3,-24)).close().assemble().finalize().extrude(-190).union(w0.sketch().arc((-99,41),(21,-98),(69,75)).arc((2,19),(-99,41)).assemble().finalize().extrude(-12))