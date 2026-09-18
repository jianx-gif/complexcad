import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,32,0))
w1=cq.Workplane('YZ',origin=(69,0,0))
r=w0.sketch().push([(0,42)]).circle(38).circle(31,mode='s').finalize().extrude(-62).union(w0.sketch().segment((-40,-1),(-10,-16)).segment((-8,-12)).arc((46,6),(52,63)).segment((54,67)).segment((24,82)).segment((22,78)).arc((-42,81),(-38,16)).arc((-38,10),(-37,4)).close().assemble().push([(0,42)]).circle(38,mode='s').finalize().extrude(-27)).union(w1.workplane(offset=-169/2).moveTo(-29,30).cylinder(169,3))