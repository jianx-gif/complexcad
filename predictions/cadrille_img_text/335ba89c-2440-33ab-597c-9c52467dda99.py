import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-42,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-76,-70),(-74,-70)).segment((-74,-73)).segment((-70,-73)).segment((-68,-90)).segment((76,-75)).segment((76,-73)).segment((74,-73)).segment((74,-70)).segment((76,-70)).segment((76,-58)).segment((-76,-71)).close().assemble().finalize().extrude(122).union(w1.sketch().arc((-100,-89),(-8,-91),(73,-36)).segment((-73,-36)).arc((-80,-40),(-87,-36)).segment((-100,-36)).close().assemble().finalize().extrude(-194))