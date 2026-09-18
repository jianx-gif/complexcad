import cadquery as cq
w0=cq.Workplane('YZ',origin=(79,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-44,-24),(0,1),(44,-24)).arc((0,46),(-44,-24)).assemble().finalize().extrude(-157).union(w0.sketch().circle(86).circle(39,mode='s').finalize().extrude(-65)).union(w1.sketch().segment((-92,-40),(-90,-40)).arc((0,-100),(90,-40)).segment((92,-40)).segment((92,-36)).arc((100,0),(92,36)).segment((92,40)).segment((90,40)).arc((0,100),(-90,40)).segment((-92,40)).segment((-92,36)).arc((-100,0),(-92,-36)).close().assemble().finalize().extrude(-14))