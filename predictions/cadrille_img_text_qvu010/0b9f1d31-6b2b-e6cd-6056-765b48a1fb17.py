import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-100,-17),(-24,-100)).segment((100,17)).segment((24,100)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-74,-49),(-64,-83),(-34,-68)).arc((54,59),(-74,-49)).assemble().finalize().extrude(-157))