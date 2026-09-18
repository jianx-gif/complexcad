import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('XY',origin=(0,0,24))
r=w0.sketch().segment((38,64),(38,79)).arc((-69,-70),(55,70)).segment((55,64)).close().assemble().finalize().extrude(-24).union(w1.sketch().segment((31,-10),(51,-10)).segment((51,10)).segment((31,10)).arc((32,0),(31,-10)).assemble().finalize().extrude(-48))