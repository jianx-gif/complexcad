import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-78,-46),(-75,-47),(-73,-48)).segment((-73,-46)).close().assemble().finalize().extrude(89).union(w1.sketch().arc((-80,-43),(-51,-39),(-24,-29)).segment((-24,-25)).segment((-19,-25)).arc((-1,16),(80,19)).arc((-10,33),(-80,-43)).assemble().finalize().extrude(-200))