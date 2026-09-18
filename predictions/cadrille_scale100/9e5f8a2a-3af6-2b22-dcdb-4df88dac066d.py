import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().rect(90,90).push([(-11,11)]).circle(16,mode='s').finalize().extrude(-5).union(w0.sketch().segment((-28,14),(-28,15)).arc((-29,11),(-26,14)).close().assemble().finalize().extrude(1))