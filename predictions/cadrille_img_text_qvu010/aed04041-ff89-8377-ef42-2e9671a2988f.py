import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('XY',origin=(0,0,-92))
r=w0.sketch().push([(0,-5)]).rect(200,190).circle(99,mode='s').circle(48).finalize().extrude(45).union(w1.sketch().arc((-3,-92),(3,0),(-3,92)).close().assemble().finalize().extrude(185))