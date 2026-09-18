import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(26,0,0))
r=w0.sketch().arc((-70,10),(-5,-78),(70,-10)).arc((0,-48),(-70,-10)).close().assemble().finalize().extrude(-181).union(w1.sketch().segment((-29,-100),(29,-100)).segment((29,-83)).arc((0,-89),(-29,-83)).close().assemble().finalize().extrude(74))