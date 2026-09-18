import cadquery as cq
w0=cq.Workplane('YZ',origin=(70,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-58,-50),(-36,-50)).segment((-58,-23)).close().assemble().finalize().extrude(-166).union(w0.sketch().segment((54,-65),(58,-65)).segment((58,-50)).close().assemble().finalize().extrude(-101)).union(w1.sketch().segment((-71,1),(18,1)).arc((19,11),(21,21)).segment((-71,21)).close().assemble().finalize().extrude(-200))