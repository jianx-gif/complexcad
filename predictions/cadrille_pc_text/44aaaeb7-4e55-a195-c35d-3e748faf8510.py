import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-100,-18),(-86,-18)).segment((-86,-35)).segment((100,-35)).segment((100,35)).segment((-86,35)).segment((-86,17)).segment((-100,17)).close().assemble().push([(-43,-29)]).circle(2,mode='s').finalize().extrude(-4).union(w0.sketch().segment((-45,26),(45,26)).arc((0,45),(-45,26)).assemble().finalize().extrude(2))