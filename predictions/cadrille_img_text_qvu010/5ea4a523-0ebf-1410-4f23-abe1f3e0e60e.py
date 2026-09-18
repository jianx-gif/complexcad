import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,-28,0))
r=w0.sketch().arc((-63,-45),(-19,-62),(26,-64)).segment((26,-59)).segment((63,-59)).segment((63,-45)).close().assemble().reset().face(w0.sketch().segment((-63,45),(16,45)).arc((-23,62),(-63,45)).assemble()).finalize().extrude(-200).union(w1.sketch().push([(0,1)]).circle(11).circle(6,mode='s').finalize().extrude(56))