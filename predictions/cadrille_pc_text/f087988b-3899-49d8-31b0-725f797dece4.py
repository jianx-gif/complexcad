import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((28,-96),(28,-77)).segment((54,-77)).segment((54,-84)).arc((-43,90),(28,-96)).assemble().finalize().extrude(-24).union(w0.workplane(offset=20/2).cylinder(20,38))