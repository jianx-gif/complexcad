import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('YZ',origin=(81,0,0))
r=w0.sketch().arc((-50,86),(-39,52),(-35,17)).segment((87,17)).arc((30,52),(-33,86)).close().assemble().finalize().extrude(48).union(w0.sketch().arc((18,-17),(64,-45),(88,4)).close().assemble().finalize().extrude(59)).union(w1.sketch().arc((-59,-36),(-41,-45),(-23,-51)).segment((-23,92)).arc((-41,86),(-56,76)).arc((-53,20),(-59,-36)).assemble().finalize().extrude(-116))