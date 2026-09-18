import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,81,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-11,-26),(11,-10),(38,-3)).arc((3,25),(-11,-20)).close().assemble().reset().face(w0.sketch().arc((12,-2),(18,1),(25,2)).arc((16,13),(12,-2)).assemble(),mode='s').finalize().extrude(-162).union(w0.sketch().push([(18,27)]).circle(48).circle(41,mode='s').finalize().extrude(-129)).union(w1.sketch().arc((-71,-59),(59,72),(-37,-80)).arc((-20,-78),(-8,-67)).arc((47,59),(-59,-30)).arc((-72,-42),(-71,-59)).assemble().finalize().extrude(-22))