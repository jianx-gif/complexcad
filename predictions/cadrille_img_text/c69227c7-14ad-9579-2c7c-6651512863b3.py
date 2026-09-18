import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,97,0))
w1=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().circle(100).circle(77,mode='s').finalize().extrude(-194).union(w1.sketch().segment((-99,-10),(-58,-10)).arc((0,-59),(58,-10)).segment((99,-10)).segment((99,10)).segment((58,10)).arc((0,59),(-58,10)).segment((-99,10)).close().assemble().finalize().extrude(-97))