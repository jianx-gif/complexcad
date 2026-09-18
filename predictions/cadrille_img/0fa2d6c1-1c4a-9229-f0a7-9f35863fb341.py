import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,89,0))
r=w0.sketch().arc((-36,-51),(0,-61),(36,-51)).close().assemble().reset().face(w0.sketch().segment((-36,51),(36,51)).arc((0,61),(-36,51)).assemble()).finalize().extrude(-161).union(w1.sketch().segment((-59,-65),(-59,-59)).arc((0,-79),(59,-59)).segment((59,-65)).arc((100,0),(59,65)).segment((59,59)).arc((0,79),(-59,59)).segment((-59,65)).arc((-100,0),(-59,-65)).assemble().circle(79,mode='s').finalize().extrude(-164))