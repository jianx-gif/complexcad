import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-43,0))
w1=cq.Workplane('ZX',origin=(0,-97,0))
r=w0.sketch().arc((-69,-49),(94,-31),(-13,88)).arc((-94,33),(-69,-49)).assemble().push([(14,-1)]).circle(73,mode='s').finalize().extrude(11).union(w0.workplane(offset=106/2).moveTo(-24,33).cylinder(106,43)).union(w1.sketch().arc((-48,-49),(-46,-48),(-45,-48)).arc((-45,-47),(-44,-46)).arc((-43,-45),(-42,-45)).arc((-39,-45),(-38,-48)).arc((-37,-49),(-37,-50)).arc((-36,-51),(-36,-53)).arc((-35,48),(-48,-49)).assemble().push([(59,48)]).circle(21,mode='s').finalize().extrude(12))