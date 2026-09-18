import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,-50,0))
r=w0.sketch().arc((-94,-66),(0,-99),(94,-66)).close().assemble().reset().face(w0.sketch().segment((-94,66),(94,66)).arc((0,99),(-94,66)).assemble()).finalize().extrude(-200).union(w1.sketch().push([(0,0.5)]).rect(122,153).push([(-43,-33)]).circle(8,mode='s').push([(0,0)]).circle(49,mode='s').finalize().extrude(150))