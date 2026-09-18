import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,36,0))
w1=cq.Workplane('ZX',origin=(0,60,0))
r=w0.sketch().push([(11,12)]).circle(89).circle(71,mode='s').finalize().extrude(-72).union(w1.sketch().arc((55,-84),(100,1),(55,86)).segment((55,39)).arc((77,1),(55,-37)).close().assemble().finalize().extrude(-120))