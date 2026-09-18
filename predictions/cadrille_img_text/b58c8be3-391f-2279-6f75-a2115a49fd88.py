import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('YZ',origin=(45,0,0))
r=w0.sketch().push([(10,10)]).circle(90).circle(75,mode='s').circle(53).finalize().extrude(-43).union(w0.sketch().arc((-59,-96),(10,-73),(79,-74)).arc((-10,99),(-59,-96)).assemble().finalize().extrude(154)).union(w1.sketch().push([(10,0)]).circle(87).circle(53,mode='s').finalize().extrude(-134))