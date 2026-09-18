import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,27))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-31,-62),(-16,-62)).segment((-16,-38)).arc((-7,-26),(-16,-14)).segment((-16,62)).segment((-31,62)).segment((-31,-18)).arc((-33,-26),(-31,-34)).close().assemble().push([(-23,0)]).circle(6,mode='s').finalize().extrude(-54).union(w1.sketch().segment((-6,-49),(10,-49)).segment((10,43)).arc((2,49),(-6,43)).close().assemble().push([(2,-17)]).circle(8,mode='s').finalize().extrude(200))