import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,97))
w1=cq.Workplane('ZX',origin=(0,63,0))
r=w0.sketch().arc((-29,32),(58,-45),(13,62)).arc((-10,49),(-29,32)).assemble().finalize().extrude(-167).union(w1.sketch().arc((-71,43),(100,1),(-69,47)).arc((-69,45),(-71,43)).assemble().push([(14,11)]).circle(78,mode='s').finalize().extrude(-129))