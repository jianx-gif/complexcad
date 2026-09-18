import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('ZX',origin=(0,73,0))
r=w0.sketch().arc((-100,-96),(0,-69),(100,-96)).segment((100,96)).segment((-100,96)).close().assemble().finalize().extrude(-34).union(w1.sketch().circle(89).reset().face(w1.sketch().segment((-50,-46),(-38,-46)).arc((0,-58),(38,-46)).segment((50,-46)).segment((50,-38)).arc((78,19),(50,76)).segment((50,84)).segment((38,84)).arc((0,96),(-38,84)).segment((-50,84)).segment((-50,76)).arc((-78,19),(-50,-38)).close().assemble(),mode='s').finalize().extrude(-142))