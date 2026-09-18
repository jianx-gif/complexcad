import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(38).circle(30,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-37,-24),(-25,-24)).arc((0,-34),(25,-24)).segment((37,-24)).segment((37,24)).segment((25,24)).arc((0,34),(-25,24)).segment((-37,24)).close().assemble().rect(36,20,mode='s').finalize().extrude(-192))