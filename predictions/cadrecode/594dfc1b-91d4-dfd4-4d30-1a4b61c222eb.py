import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
w1=cq.Workplane('XY',origin=(0,0,-23))
r=w0.sketch().arc((-98,-19),(-94,-28),(-94,-37)).arc((96,28),(-98,-19)).assemble().push([(-75,-1)]).circle(7,mode='s').push([(-4,83)]).circle(16,mode='s').finalize().extrude(72).union(w0.sketch().push([(0,-1)]).circle(89).push([(0,-0.5)]).rect(38,163,mode='s').finalize().extrude(125)).union(w1.workplane(offset=98/2).cylinder(98,70))