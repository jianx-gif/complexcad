import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-63,0))
w1=cq.Workplane('XY',origin=(0,0,-61))
r=w0.sketch().circle(100).circle(91,mode='s').finalize().extrude(12).union(w0.sketch().arc((-99,-18),(0,-99),(99,-18)).segment((98,-18)).arc((0,-98),(-98,-18)).close().assemble().reset().face(w0.sketch().segment((-99,18),(-98,18)).arc((0,98),(98,18)).segment((99,18)).arc((0,99),(-99,18)).assemble()).finalize().extrude(163)).union(w1.sketch().push([(0,-54)]).circle(46).push([(1,-54)]).circle(20,mode='s').finalize().extrude(138))