import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,32,0))
w1=cq.Workplane('YZ',origin=(77,0,0))
r=w0.sketch().push([(0,42)]).circle(38).circle(31,mode='s').finalize().extrude(-61).union(w0.sketch().segment((-40,-1),(-10,-16)).segment((-8,-12)).arc((46,6),(50,63)).segment((52,67)).segment((22,82)).segment((20,78)).arc((-43,79),(-39,13)).arc((-39,6),(-38,-1)).close().assemble().push([(0,42)]).circle(38,mode='s').finalize().extrude(-27)).union(w1.workplane(offset=-177/2).moveTo(-29,30).cylinder(177,3))