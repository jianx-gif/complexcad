import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,84,0))
r=w0.sketch().segment((-32,-11),(-19,-11)).arc((0,-21),(19,-11)).segment((32,-11)).segment((32,11)).segment((19,11)).arc((0,21),(-19,11)).segment((-32,11)).close().assemble().finalize().extrude(-195).union(w1.sketch().segment((-28,-87),(-28,-84)).arc((-86,0),(-28,84)).segment((-28,87)).arc((-100,0),(-28,-87)).assemble().reset().face(w1.sketch().arc((28,-87),(100,0),(28,87)).segment((28,84)).arc((86,0),(28,-84)).close().assemble()).finalize().extrude(-164))