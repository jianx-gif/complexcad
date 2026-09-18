import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,27,0))
r=w0.sketch().arc((-96,-29),(-92,-31),(-88,-33)).arc((94,-34),(-35,88)).arc((-67,63),(-96,33)).segment((-73,33)).arc((-78,0),(-73,-33)).arc((-77,-31),(-81,-29)).close().assemble().finalize().extrude(-156).union(w0.sketch().segment((-55,-95),(-25,-95)).arc((-44,-79),(-55,-58)).close().assemble().finalize().extrude(-100)).union(w1.sketch().arc((-60,-44),(-51,-46),(-44,-51)).arc((53,79),(-60,-44)).assemble().push([(14,33)]).circle(2,mode='s').finalize().extrude(-104))