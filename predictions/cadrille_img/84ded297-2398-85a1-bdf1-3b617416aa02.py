import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(-81,0)]).circle(13).push([(72,0)]).circle(13).finalize().extrude(-28).union(w0.sketch().segment((-29,16),(-27,14)).segment((1,42)).segment((-1,44)).close().assemble().finalize().extrude(90)).union(w1.sketch().arc((-66,-11),(0,-61),(91,-40)).segment((91,-38)).arc((93,-30),(94,-22)).arc((95,-20),(94,-18)).arc((94,1),(91,19)).segment((91,21)).segment((-66,21)).segment((-66,19)).arc((-68,4),(-66,-11)).assemble().finalize().extrude(200))