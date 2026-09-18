import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-39,-62),(-36,-64),(-34,-67)).arc((37,64),(-39,-62)).assemble().finalize().extrude(197).union(w1.sketch().segment((-41,-77),(-39,-77)).arc((0,-84),(39,-77)).segment((41,-77)).segment((41,-76)).arc((84,0),(41,76)).segment((41,77)).segment((39,77)).arc((0,84),(-39,77)).segment((-41,77)).segment((-41,76)).arc((-84,0),(-41,-76)).close().assemble().circle(83,mode='s').finalize().extrude(184))