import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('YZ',origin=(39,0,0))
r=w0.sketch().push([(78,21)]).circle(22).circle(15,mode='s').finalize().extrude(28).union(w0.sketch().arc((-100,0),(-98,-1),(-97,-3)).arc((100,1),(-97,3)).arc((-98,1),(-100,1)).close().assemble().finalize().extrude(159)).union(w1.sketch().arc((-69,73),(0,-91),(69,73)).close().assemble().push([(0,3)]).circle(85,mode='s').finalize().extrude(-14))