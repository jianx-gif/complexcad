import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-26,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-99,-10),(-95,-12),(-91,-14)).arc((-93,-1),(-93,12)).arc((-97,1),(-99,-10)).assemble().finalize().extrude(95).union(w0.sketch().arc((91,-21),(95,-34),(96,-47)).segment((100,-47)).segment((100,-21)).close().assemble().finalize().extrude(126)).union(w1.sketch().segment((-87,-67),(54,-67)).arc((55,-62),(57,-57)).segment((-87,-57)).close().assemble().finalize().extrude(-200))