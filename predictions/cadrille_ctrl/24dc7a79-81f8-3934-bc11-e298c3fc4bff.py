import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-44,-1),(-40,-19)).segment((-17,-14)).segment((-17,20)).segment((-40,20)).segment((-40,1)).close().assemble().finalize().extrude(-5).union(w0.sketch().segment((-27,-15),(40,-21)).segment((44,19)).segment((-23,25)).close().assemble().finalize().extrude(-4)).union(w0.sketch().segment((-24,-12),(-17,-12)).segment((-17,1)).segment((-24,1)).segment((-24,-2)).arc((-23,-3),(-24,-4)).close().assemble().push([(42,1)]).circle(2).finalize().extrude(19))
