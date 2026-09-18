import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((43,15),(71,1)).segment((71,57)).segment((43,57)).close().assemble().finalize().extrude(-8).union(w1.sketch().segment((-57,-6),(29,-6)).arc((25,0),(23,2)).segment((-51,2)).arc((-54,-2),(-57,-6)).assemble().finalize().extrude(-200))