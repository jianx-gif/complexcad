import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-10,0))
w1=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().segment((-100,39),(-84,39)).arc((-77,57),(-66,73)).segment((-100,73)).close().assemble().reset().face(w0.sketch().arc((-65,-40),(100,-11),(-43,80)).arc((-48,79),(-53,76)).segment((-53,73)).segment((-57,73)).arc((-62,57),(-65,39)).segment((-53,39)).segment((-53,-40)).close().assemble()).push([(18,8)]).circle(82,mode='s').finalize().extrude(-28).union(w1.sketch().arc((13,-5),(14,0),(13,5)).close().assemble().finalize().extrude(127))