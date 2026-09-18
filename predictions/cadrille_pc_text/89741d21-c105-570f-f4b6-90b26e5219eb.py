import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('ZX',origin=(0,34,0))
r=w0.sketch().segment((-34,-10),(-18,-10)).arc((18,-45),(18,6)).segment((18,2)).segment((-34,2)).close().assemble().push([(-10,-6)]).circle(9,mode='s').finalize().extrude(95).union(w0.workplane(offset=144/2).moveTo(0,2).cylinder(144,19)).union(w1.sketch().arc((-98,15),(98,-16),(-94,32)).arc((-75,19),(-98,15)).assemble().push([(2,0)]).circle(11,mode='s').finalize().extrude(-9))