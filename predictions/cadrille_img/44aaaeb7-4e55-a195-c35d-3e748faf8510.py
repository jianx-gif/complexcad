import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(-65,37)]).circle(53).circle(19,mode='s').push([(36,53)]).circle(17).circle(13,mode='s').finalize().extrude(-7).union(w1.sketch().arc((-84,-50),(0,-69),(84,-50)).segment((84,-48)).arc((0,-67),(-84,-48)).close().assemble().reset().face(w1.sketch().arc((-84,48),(0,67),(84,48)).segment((84,50)).arc((0,69),(-84,48)).assemble()).finalize().extrude(200))