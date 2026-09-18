import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().arc((-62,24),(64,-17),(-58,33)).arc((-43,21),(-62,24)).assemble().push([(-19,-26)]).circle(22,mode='s').push([(-11,29)]).circle(16,mode='s').finalize().extrude(-60).union(w0.sketch().circle(100).push([(-50.5,0)]).rect(83,16,mode='s').finalize().extrude(-27))