import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,19,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-52,21),(-51,21)).arc((-32,43),(-7,57)).segment((-7,58)).segment((-5,58)).arc((2,59),(9,58)).segment((11,58)).segment((11,57)).arc((36,43),(55,21)).segment((84,21)).arc((17,57),(-52,21)).assemble().finalize().extrude(57).union(w1.sketch().arc((-80,-59),(-75,-60),(-70,-61)).arc((-16,-21),(38,-61)).arc((64,-49),(80,-26)).segment((80,-59)).close().assemble().finalize().extrude(-200))