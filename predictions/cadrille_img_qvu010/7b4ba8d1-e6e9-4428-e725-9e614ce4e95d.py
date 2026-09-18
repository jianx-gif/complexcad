import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('YZ',origin=(61,0,0))
r=w0.sketch().push([(0,1)]).circle(60).circle(54,mode='s').finalize().extrude(-106).union(w1.sketch().arc((-96,-100),(-92,-100),(-88,-99)).arc((-92,-97),(-96,-95)).close().assemble().reset().face(w1.sketch().arc((-49,99),(-45,97),(-41,95)).arc((45,90),(96,23)).arc((92,24),(88,24)).arc((45,90),(-33,96)).arc((-41,99),(-49,99)).assemble()).finalize().extrude(-148))