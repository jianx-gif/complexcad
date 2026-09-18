import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('ZX',origin=(0,44,0))
r=w0.sketch().arc((-59,-59),(12,21),(100,-35)).arc((98,-29),(95,-24)).segment((95,-19)).segment((91,-19)).arc((0,38),(-59,-59)).assemble().finalize().extrude(-111).union(w1.sketch().arc((-100,89),(-1,23),(88,-94)).arc((45,53),(-100,89)).assemble().finalize().extrude(-36))