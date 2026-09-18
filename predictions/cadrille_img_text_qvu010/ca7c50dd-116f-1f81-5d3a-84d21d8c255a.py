import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-74,-51),(-57,8),(-74,67)).segment((-74,48)).arc((-67,8),(-74,-32)).close().assemble().reset().face(w0.sketch().arc((47,-67),(74,-8),(57,51)).segment((57,48)).arc((64,8),(57,-32)).segment((57,-67)).close().assemble()).finalize().extrude(-145).union(w1.sketch().segment((-95,21),(-21,21)).arc((-57,57),(-21,94)).segment((-95,94)).close().assemble().finalize().extrude(-200))