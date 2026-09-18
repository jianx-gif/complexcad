import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((15,5),(35,5)).arc((25,10),(15,5)).assemble().finalize().extrude(-14).union(w1.sketch().arc((-50,-6),(-49,-6),(-48,-7)).segment((48,-7)).segment((48,-6)).segment((50,-6)).segment((50,22)).segment((48,22)).segment((48,23)).segment((43,23)).segment((43,0)).segment((-43,0)).segment((-43,22)).segment((-48,22)).segment((-48,21)).segment((-50,21)).close().assemble().finalize().extrude(-200))