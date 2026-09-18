import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-17,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,12)]).circle(17).circle(13,mode='s').finalize().extrude(49).union(w1.sketch().arc((-99,-27),(0,-82),(99,-27)).segment((67,-27)).arc((0,-68),(-67,-27)).close().assemble().finalize().extrude(-181))