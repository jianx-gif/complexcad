import cadquery as cq
w0=cq.Workplane('YZ',origin=(-60,0,0))
w1=cq.Workplane('XY',origin=(0,0,-66))
r=w0.sketch().arc((-59,-72),(0,-91),(59,-72)).segment((59,-39)).arc((71,0),(59,39)).segment((59,72)).arc((0,91),(-59,72)).segment((-59,39)).arc((-71,0),(-59,-39)).close().assemble().push([(13,36)]).circle(42,mode='s').finalize().extrude(150).union(w1.sketch().arc((-53,-69),(0,-87),(53,-69)).segment((39,-69)).arc((71,0),(39,69)).segment((53,69)).arc((0,87),(-53,69)).segment((-39,69)).arc((-71,0),(-39,-69)).close().assemble().finalize().extrude(166))