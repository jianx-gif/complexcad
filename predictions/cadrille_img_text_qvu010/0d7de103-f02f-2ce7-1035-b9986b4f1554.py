import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-85,-11),(-83,-14)).segment((85,11)).segment((83,14)).close().assemble().finalize().extrude(133).union(w1.sketch().arc((-95,-35),(0,-95),(95,-35)).segment((67,-35)).arc((0,-80),(-67,-35)).close().assemble().finalize().extrude(-200))