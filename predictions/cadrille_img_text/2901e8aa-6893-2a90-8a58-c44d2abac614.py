import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-66,0))
r=w0.sketch().push([(0,22)]).circle(70).circle(29,mode='s').finalize().extrude(19).union(w0.sketch().arc((-65,-39),(-47,-58),(-43,-84)).arc((-16,-68),(-1,-41)).arc((-34,-48),(-65,-39)).assemble().finalize().extrude(198)).union(w1.sketch().arc((-36,-33),(14,-1),(55,42)).arc((1,33),(-36,-3)).close().assemble().finalize().extrude(166))