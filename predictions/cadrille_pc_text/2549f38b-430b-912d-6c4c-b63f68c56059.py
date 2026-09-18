import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,11))
w1=cq.Workplane('XY',origin=(0,0,7))
r=w0.sketch().segment((-56,-34),(33,-34)).segment((33,34)).segment((-56,34)).segment((-56,-1)).segment((-39,-1)).segment((-39,-3)).segment((-56,-3)).close().assemble().finalize().extrude(-16).union(w1.sketch().segment((-100,-32),(100,-32)).segment((100,32)).segment((-100,32)).segment((-100,-31)).arc((-98,-31),(-100,-32)).assemble().circle(16,mode='s').finalize().extrude(-18))