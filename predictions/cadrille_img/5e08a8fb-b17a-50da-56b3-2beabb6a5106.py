import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-50,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(24,33)]).circle(17).circle(14,mode='s').finalize().extrude(14).union(w1.sketch().arc((-98,-62),(-89,-63),(-79,-64)).arc((-78,-64),(-77,-63)).arc((0,-91),(77,-63)).arc((78,-63),(78,-62)).arc((89,-61),(98,-60)).segment((98,62)).arc((89,63),(79,64)).arc((78,64),(77,65)).arc((78,63),(78,62)).arc((0,91),(-78,62)).arc((-89,61),(-98,60)).close().assemble().finalize().extrude(-200))