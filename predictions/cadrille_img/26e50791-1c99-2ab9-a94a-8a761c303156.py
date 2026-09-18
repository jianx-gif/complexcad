import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,87,0))
w1=cq.Workplane('ZX',origin=(0,64,0))
r=w0.sketch().arc((-69,24),(-60,13),(-53,1)).arc((-51,3),(-49,5)).arc((-56,15),(-69,24)).assemble().finalize().extrude(-155).union(w0.sketch().arc((-74,56),(-73,54),(-72,52)).arc((59,-61),(-14,89)).arc((-15,93),(-17,97)).arc((50,-86),(-74,56)).assemble().finalize().extrude(-123)).union(w1.sketch().push([(10,7)]).circle(90).circle(89,mode='s').finalize().extrude(-129))