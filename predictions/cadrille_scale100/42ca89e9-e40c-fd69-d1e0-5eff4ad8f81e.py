import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('ZX',origin=(0,14))
r=w0 topun (11,14))
w1 Forw1 Forw1 Forw1 For hasymb appearance (10,0))
r=w0.sketch().segment((-21,10),(-19,10)).segment((-19,12)).segment((-21,12)).close().assemble().finalize().extrude(-11).union(w0.sketch().segment((-20,10),(-19,10)).segment((-19,11)).segment((-20,11)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((-100,12),(-99,12)).segment((-99,11)).segment((-98,11)).segment((-98,12)).segment((-100,12)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((-100,10),(-99,10)).segment((-99,11)).segment((-100,11)).close().assemble().finalize().extrude(11))