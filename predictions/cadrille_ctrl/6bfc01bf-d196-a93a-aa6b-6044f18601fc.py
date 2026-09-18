import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,7,0))
w1=cq.Workplane('XY',origin=(0,0,24))
r=w0.sketch().segment((33,-23),(80,-45)).segment((80,-40)).arc((62,-11),(80,17)).segment((80,45)).segment((74,45)).segment((74,31)).segment((46,31)).close().assemble().reset().face(w0.sketch().segment((38,13),(48,-25)).segment((78,-17)).segment((68,21)).close().assemble(),mode='s').finalize().extrude(-14).union(w0.sketch().push([(20,-1)]).circle(20).circle(12,mode='s').finalize().extrude(-7)).union(w1.sketch().push([(0,-1)]).circle(7).circle(5,mode='s').finalize().extrude(-23))
