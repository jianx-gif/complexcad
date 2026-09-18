import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('XY',origin=(0,0,58))
r=w0.sketch().arc((-62,-59),(0,-82),(62,-59)).segment((59,-59)).arc((0,-81),(-59,-59)).close().assemble().reset().face(w0.sketch().segment((-62,59),(-59,59)).arc((0,81),(59,59)).segment((62,59)).arc((0,82),(-62,59)).assemble()).finalize().extrude(-155).union(w1.sketch().circle(100).rect(100,110,mode='s').finalize().extrude(-138))