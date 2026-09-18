import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,3))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-60,45),(-59,-45)).segment((59,-44)).segment((59,45)).close().assemble().push([(-35,-20)]).circle(2,mode='s').push([(43,-19)]).circle(3,mode='s').finalize().extrude(-8).union(w0.workplane(offset=5/2).cylinder(5,30)).union(w1.workplane(offset=200/2).moveTo(-4.5,2).box(7,4,200))