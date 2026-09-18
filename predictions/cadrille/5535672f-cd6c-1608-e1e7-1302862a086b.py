import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().rect(140,200).push([(-40,31)]).circle(4,mode='s').finalize().extrude(-16).union(w0.sketch().segment((-45,-11),(-45,11)).arc((-46,0),(-45,-11)).assemble().reset().face(w0.sketch().arc((45,-11),(46,0),(45,11)).close().assemble()).finalize().extrude(8))