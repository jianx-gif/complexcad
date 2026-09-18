import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().arc((-39,10),(39,-10),(-38,13)).arc((-35,11),(-39,10)).assemble().push([(0,-1)]).circle(12,mode='s').finalize().extrude(-27).union(w0.sketch().segment((-43,-1),(-38,-6)).arc((-26,-31),(-1,-40)).segment((4,-45)).segment((10,-39)).arc((31,-25),(39,-1)).segment((43,4)).segment((38,9)).arc((26,33),(1,42)).segment((-4,47)).segment((-10,41)).arc((-31,28),(-39,4)).close().assemble().finalize().extrude(-26)).union(w0.workplane(offset=2/2).moveTo(0,-1).cylinder(2,41))
