import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().arc((-39,10),(-37,12),(-34,14)).arc((35,-1),(-33,-12)).arc((-36,-11),(-38,-9)).arc((40,1),(-39,10)).assemble().finalize().extrude(-20).union(w0.sketch().segment((-15,-32),(-15,-31)).segment((-13,-31)).segment((-13,-33)).arc((14,38),(-15,-32)).assemble().push([(0,1)]).circle(35,mode='s').finalize().extrude(-20))
