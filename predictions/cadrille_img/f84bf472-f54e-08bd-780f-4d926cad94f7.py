import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().arc((-60,32),(18,73),(84,13)).arc((85,15),(87,17)).arc((-18,89),(-48,-29)).arc((-43,-27),(-39,-24)).arc((15,-46),(69,-25)).arc((68,-27),(67,-29)).arc((66,-31),(65,-32)).arc((66,-30),(67,-28)).arc((18,46),(-60,32)).assemble().finalize().extrude(-48).union(w1.sketch().push([(10,10)]).circle(90).circle(86,mode='s').finalize().extrude(-79))