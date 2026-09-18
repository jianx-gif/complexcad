import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,44,0))
w1=cq.Workplane('XY',origin=(0,0,-79))
r=w0.sketch().arc((25,-100),(79,-36),(90,47)).segment((69,18)).arc((65,-11),(43,-31)).close().assemble().finalize().extrude(-144).union(w1.sketch().push([(0,22)]).circle(78).circle(74,mode='s').finalize().extrude(179))