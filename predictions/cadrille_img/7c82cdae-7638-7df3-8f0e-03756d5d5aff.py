import cadquery as cq
w0=cq.Workplane('YZ',origin=(-75,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-78,28),(-71,30),(-64,32)).arc((-10,78),(14,11)).arc((25,-2),(34,-17)).arc((-10,81),(-78,28)).assemble().finalize().extrude(101).union(w1.sketch().segment((-81,15),(81,15)).segment((81,20)).arc((0,34),(-81,20)).close().assemble().finalize().extrude(-200))