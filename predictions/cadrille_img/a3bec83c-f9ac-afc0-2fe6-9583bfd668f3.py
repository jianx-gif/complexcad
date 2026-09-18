import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-26,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(-53,19.5)]).rect(86,155).push([(-53,20)]).circle(22,mode='s').push([(53,19)]).circle(11,mode='s').finalize().extrude(10).union(w1.sketch().arc((-98,-40),(0,-81),(98,-40)).segment((76,-40)).arc((0,-78),(-76,-40)).close().assemble().reset().face(w1.sketch().segment((-98,40),(-76,40)).arc((0,78),(76,40)).segment((98,40)).arc((0,81),(-98,40)).assemble()).finalize().extrude(-200))