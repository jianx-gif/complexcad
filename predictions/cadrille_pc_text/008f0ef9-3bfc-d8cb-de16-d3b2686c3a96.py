import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-10),(-39,-10)).arc((-34,-9),(-30,-10)).segment((75,-10)).segment((75,10)).segment((63,10)).segment((63,2)).segment((-63,2)).segment((-63,10)).segment((-75,10)).close().assemble().finalize().extrude(-200)