import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,9,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().push([(0,27)]).circle(73).push([(61,31)]).circle(33,mode='s').finalize().extrude(-18).union(w1.sketch().arc((-100,-10),(-70,-19),(-38,-23)).arc((-35,-1),(-28,20)).arc((-55,35),(-78,57)).arc((-89,60),(-100,62)).close().assemble().finalize().extrude(-200))