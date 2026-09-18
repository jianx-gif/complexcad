import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,87,0))
w1=cq.Workplane('YZ',origin=(-67,0,0))
r=w0.sketch().arc((-100,-19),(-29,-1),(33,-40)).arc((45,-31),(54,-19)).segment((34,-19)).arc((0,-36),(-34,-19)).close().assemble().finalize().extrude(-108).union(w1.sketch().arc((-97,-46),(-19,21),(57,-50)).arc((77,0),(57,50)).segment((57,100)).segment((-57,100)).segment((-57,50)).arc((-83,5),(-97,-46)).assemble().finalize().extrude(135))