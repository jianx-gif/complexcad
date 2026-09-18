import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().push([(0,-54)]).rect(140,92).push([(-41,31)]).circle(4,mode='s').finalize().extrude(-16).union(w0.sketch().segment((-45,-12),(-45,12)).arc((-47,0),(-45,-12)).assemble().reset().face(w0.sketch().arc((45,-12),(47,0),(45,12)).close().assemble()).finalize().extrude(8))