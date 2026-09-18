import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-79,53),(-67,63),(-53,71)).segment((-79,71)).close().assemble().finalize().extrude(110).union(w1.sketch().arc((-99,-29),(0,-73),(99,-29)).segment((38,-29)).arc((0,-45),(-38,-29)).close().assemble().finalize().extrude(-183))