import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-92,-4),(-89,-27),(-80,-48)).segment((-80,-18)).arc((-60,-41),(-33,-53)).segment((-33,-87)).arc((27,-61),(57,-4)).segment((51,-4)).arc((0,-51),(-51,-4)).close().assemble().reset().face(w0.sketch().segment((-57,4),(-51,4)).arc((0,51),(51,4)).segment((57,4)).arc((0,51),(-57,4)).assemble()).finalize().extrude(-200)