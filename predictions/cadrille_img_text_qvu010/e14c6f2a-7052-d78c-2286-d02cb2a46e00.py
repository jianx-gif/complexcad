import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(75).circle(54,mode='s').finalize().extrude(-180).union(w1.sketch().arc((-91,-35),(0,-94),(91,-35)).segment((67,-35)).arc((0,-81),(-67,-35)).close().assemble().reset().face(w1.sketch().segment((-91,35),(-67,35)).arc((0,81),(67,35)).segment((91,35)).arc((0,94),(-91,35)).assemble()).finalize().extrude(-200))