import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,96))
r=w0.sketch().segment((-61,-2),(-55,-2)).arc((0,-55),(55,-2)).segment((61,-2)).segment((61,2)).segment((55,2)).arc((0,55),(-55,2)).segment((-61,2)).close().assemble().finalize().extrude(-4).union(w1.sketch().arc((-37,-10),(-20,-27),(3,-32)).arc((10,-28),(18,-26)).arc((28,18),(-15,32)).arc((-27,13),(-37,-10)).assemble().push([(21,10)]).circle(10,mode='s').finalize().extrude(-196))