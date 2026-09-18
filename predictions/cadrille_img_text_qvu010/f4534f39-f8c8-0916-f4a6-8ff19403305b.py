import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().circle(94).circle(89,mode='s').circle(57).finalize().extrude(-27).union(w1.sketch().arc((-39,-38),(-10,-21),(23,-14)).arc((27,12),(39,36)).arc((1,28),(-31,8)).segment((-31,-38)).close().assemble().finalize().extrude(-114))