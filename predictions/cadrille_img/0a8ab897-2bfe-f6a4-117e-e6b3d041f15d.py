import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,16,0))
r=w0.sketch().segment((-29,-11),(29,-11)).arc((0,-2),(-29,-11)).assemble().finalize().extrude(166).union(w0.sketch().segment((-68,10),(29,10)).arc((-19,35),(-29,88)).segment((-68,88)).close().assemble().finalize().extrude(165)).union(w0.sketch().arc((-59,16),(-29,35),(3,44)).arc((-39,45),(-59,16)).assemble().finalize().extrude(166)).union(w1.sketch().push([(0,26)]).rect(148,70).circle(22,mode='s').finalize().extrude(-26))