import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().arc((-35,-17),(-33,-18),(-32,-20)).arc((34,20),(-35,-17)).assemble().push([(0,0)]).circle(35,mode='s').finalize().extrude(-20).union(w0.sketch().segment((-15,-32),(-15,-31)).segment((-13,-31)).segment((-13,-33)).arc((14,37),(-15,-32)).assemble().push([(0,0)]).circle(35,mode='s').finalize().extrude(-20))