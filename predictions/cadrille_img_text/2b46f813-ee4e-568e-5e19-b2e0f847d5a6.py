import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-67,0))
w1=cq.Workplane('YZ',origin=(-48,0,0))
r=w0.sketch().push([(8,11)]).circle(89).circle(87,mode='s').finalize().extrude(19).union(w0.sketch().arc((-84,2),(-54,-59),(8,-87)).segment((8,-48)).arc((-35,-3),(-35,59)).segment((-35,60)).segment((-34,60)).arc((-12,74),(13,80)).arc((32,81),(51,78)).arc((53,78),(54,77)).arc((67,73),(78,67)).arc((12,87),(-51,68)).arc((-58,31),(-84,2)).assemble().finalize().extrude(167)).union(w1.sketch().arc((-100,-11),(-96,0),(-100,11)).close().assemble().finalize().extrude(139))