import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,49,0))
r=w0.sketch().arc((-35,49),(11,18),(58,49)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-94,0),(-70,39),(-35,68)).arc((-87,58),(-94,0)).assemble().push([(-88,23)]).circle(6,mode='s').finalize().extrude(-99))