import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,41,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(-66,53)]).circle(21).circle(13,mode='s').finalize().extrude(-89).union(w0.sketch().push([(0,11)]).circle(12).circle(9,mode='s').finalize().extrude(-11)).union(w1.sketch().arc((-100,-32),(0,-86),(100,-32)).segment((93,-32)).arc((0,-82),(-93,-32)).close().assemble().reset().face(w1.sketch().segment((-100,32),(-93,32)).arc((0,82),(93,32)).segment((100,32)).arc((0,86),(-100,32)).assemble()).finalize().extrude(-200))