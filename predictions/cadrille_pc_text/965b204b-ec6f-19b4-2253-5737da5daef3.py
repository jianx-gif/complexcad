import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().segment((-100,-57),(-84,-57)).segment((-84,-47)).segment((-22,-52)).segment((-22,-57)).segment((100,-57)).segment((100,28)).segment((-100,28)).close().assemble().finalize().extrude(-4).union(w0.sketch().segment((43,15),(71,1)).segment((71,57)).segment((43,57)).close().assemble().finalize().extrude(9))