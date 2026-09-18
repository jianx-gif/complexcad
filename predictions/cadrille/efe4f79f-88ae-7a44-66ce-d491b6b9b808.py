import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-90))
r=w0.sketch().segment((-30,-20),(20,-20)).segment((20,-18)).segment((-28,-18)).segment((-28,18)).segment((20,18)).segment((20,20)).segment((-30,20)).close().assemble().finalize().extrude(200).union(w1.sketch().segment((-28,-8),(28,-8)).segment((28,-6)).segment((30,-6)).segment((30,8)).segment((-28,8)).close().assemble().finalize().extrude(188))