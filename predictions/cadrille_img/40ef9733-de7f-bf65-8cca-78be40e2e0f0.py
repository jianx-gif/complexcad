import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((27,-61),(65,0),(27,61)).close().assemble().finalize().extrude(3).union(w1.sketch().arc((-99,24),(-40,-61),(64,-77)).arc((69,-67),(77,-61)).arc((96,25),(39,92)).arc((-44,89),(-99,24)).assemble().finalize().extrude(-111))