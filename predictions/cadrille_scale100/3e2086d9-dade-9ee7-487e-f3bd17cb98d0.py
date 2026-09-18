import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
r=w0.workplane(offset=-70/2).moveTo(-1,0).cylinder(70,1).union(w0.sketch().circle(40).push([(18,-1)]).circle(13,mode='s').finalize().extrude(35)).union(w0.sketch().arc((19,-24),(19,-16),(26,-18)).arc((-23,21),(19,-24)).assemble().push([(18,0)]).circle(8,mode='s').finalize().extrude(50))