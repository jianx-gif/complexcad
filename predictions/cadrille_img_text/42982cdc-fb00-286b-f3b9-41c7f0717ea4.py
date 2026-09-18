import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-55,-89),(-14,0),(55,80)).arc((-59,38),(-55,-89)).assemble().finalize().extrude(197).union(w1.sketch().segment((-86,-58),(48,-58)).arc((65,-1),(86,55)).segment((86,58)).segment((-86,58)).close().assemble().reset().face(w1.sketch().arc((-35,17),(-59,-31),(-10,-5)).arc((26,46),(-35,17)).assemble(),mode='s').push([(71,46)]).circle(9,mode='s').finalize().extrude(200))