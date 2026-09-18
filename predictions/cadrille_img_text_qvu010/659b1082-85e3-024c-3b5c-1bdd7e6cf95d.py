import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().arc((-100,-40),(0,-100),(100,-40)).segment((87,-40)).arc((0,-92),(-87,-40)).close().assemble().reset().face(w0.sketch().segment((-100,40),(-87,40)).arc((0,92),(87,40)).segment((100,40)).arc((0,100),(-100,40)).assemble()).finalize().extrude(-186).union(w1.sketch().circle(80).rect(64,70,mode='s').finalize().extrude(-162))