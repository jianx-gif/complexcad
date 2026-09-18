import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-15,0))
w1=cq.Workplane('XY',origin=(0,0,49))
r=w0.sketch().segment((57,12),(98,-10)).segment((100,0)).segment((77,24)).segment((77,12)).close().assemble().finalize().extrude(30).union(w1.sketch().push([(-5,0)]).circle(19).circle(15,mode='s').finalize().extrude(-149))