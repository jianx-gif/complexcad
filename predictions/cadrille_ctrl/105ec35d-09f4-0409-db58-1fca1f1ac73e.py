import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-15,-40),(15,-40)).segment((15,10)).segment((75,10)).segment((75,40)).segment((-15,40)).close().assemble().push([(30,25)]).circle(14,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-15,-10),(-15,10)).arc((-17,0),(-15,-10)).assemble().reset().face(w0.sketch().arc((3,-17),(17,0),(3,17)).close().assemble()).finalize().extrude(-8))
