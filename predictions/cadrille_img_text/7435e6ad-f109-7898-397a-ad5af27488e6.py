import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-36,86),(35,-86),(-30,88)).segment((-30,86)).close().assemble().finalize().extrude(-12).union(w1.sketch().arc((-63,-48),(0,-71),(63,-48)).segment((38,-48)).arc((67,0),(38,48)).segment((63,48)).arc((0,71),(-63,48)).segment((-38,48)).arc((-67,0),(-38,-48)).close().assemble().finalize().extrude(-194))