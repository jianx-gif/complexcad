import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('YZ',origin=(-38,0,0))
r=w0.sketch().arc((-36,-47),(-19,-66),(5,-77)).arc((19,-32),(55,-5)).arc((45,25),(23,47)).arc((11,1),(-36,-19)).arc((-33,-33),(-36,-47)).assemble().finalize().extrude(157).union(w1.sketch().segment((-100,-41),(-94,-41)).arc((0,-97),(94,-41)).segment((100,-41)).segment((100,41)).segment((94,41)).arc((0,97),(-94,41)).segment((-100,41)).close().assemble().circle(87,mode='s').finalize().extrude(74))