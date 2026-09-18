import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().arc((18,-35),(19,-34),(20,-34)).arc((19,-33),(18,-33)).close().assemble().finalize().extrude(-90).union(w0.sketch().circle(40).push([(-10,-27)]).circle(10,mode='s').finalize().extrude(-10)).union(w0.sketch().arc((18,-24),(21,-12),(29,-7)).arc((-24,17),(18,-24)).assemble().circle(8,mode='s').push([(23,0)]).circle(4,mode='s').finalize().extrude(52))
