import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('ZX',origin=(0,25,0))
r=w0.sketch().arc((-100,-77),(0,-84),(100,-77)).segment((100,77)).arc((0,84),(-100,77)).close().assemble().finalize().extrude(-194).union(w0.sketch().segment((-35,33),(-33,33)).arc((0,-34),(33,33)).segment((35,33)).segment((35,34)).segment((-35,34)).close().assemble().finalize().extrude(-109)).union(w1.sketch().circle(60).circle(33,mode='s').finalize().extrude(-10))