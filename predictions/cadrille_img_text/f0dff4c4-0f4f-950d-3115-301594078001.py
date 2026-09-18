import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,71,0))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().arc((-69,35),(-65,37),(-61,39)).arc((58,-49),(-10,78)).arc((-12,81),(-15,84)).arc((59,-81),(-69,61)).close().assemble().finalize().extrude(-129).union(w1.sketch().arc((11,-100),(43,-61),(94,-40)).arc((-57,82),(11,-84)).close().assemble().push([(18,11)]).circle(67,mode='s').finalize().extrude(-145))