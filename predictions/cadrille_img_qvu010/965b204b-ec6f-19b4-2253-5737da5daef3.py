import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-91))
r=w0.sketch().arc((-30,-48),(17,-59),(64,-48)).close().assemble().reset().face(w0.sketch().segment((-30,48),(73,24)).segment((75,34)).segment((48,40)).arc((46,40),(44,41)).segment((44,40)).segment((41,40)).segment((41,42)).arc((10,50),(-20,59)).close().assemble()).finalize().extrude(169).union(w1.sketch().segment((-75,-14),(41,-14)).segment((41,-1)).arc((21,1),(3,10)).arc((-10,10),(-21,14)).segment((-75,14)).close().assemble().finalize().extrude(191))