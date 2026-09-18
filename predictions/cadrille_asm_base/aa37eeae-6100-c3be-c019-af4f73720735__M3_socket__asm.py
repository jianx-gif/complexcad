import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-9))
w1=cq.Workplane('YZ',origin=(-78,0,0))
r=w0.sketch().segment((-89,-39),(-10,-39)).segment((-10,-52)).segment((-8,-52)).segment((-8,-39)).segment((82,-39)).segment((82,-12)).segment((100,-12)).segment((100,24)).segment((82,24)).segment((82,52)).segment((-89,52)).close().assemble().push([(92,1)]).circle(4,mode='s').finalize().extrude(24).union(w1.sketch().arc((-33,-14),(11,-13),(45,-26)).arc((12,25),(-33,-14)).assemble().finalize().extrude(-12))