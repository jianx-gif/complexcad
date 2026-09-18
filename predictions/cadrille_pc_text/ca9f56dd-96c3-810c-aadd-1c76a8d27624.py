import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('ZX',origin=(0,42,0))
r=w0.sketch().circle(83).circle(36,mode='s').finalize().extrude(-85).union(w0.sketch().arc((-100,-2),(98,-18),(-98,20)).arc((-83,3),(-100,-2)).assemble().finalize().extrude(-35)).union(w1.sketch().segment((-3,-45),(3,-45)).segment((3,-36)).arc((0,-37),(-3,-36)).close().assemble().finalize().extrude(-132))