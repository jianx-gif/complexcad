import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-63,-21),(63,-21)).segment((63,21)).segment((57,21)).segment((57,-16)).segment((-57,-16)).segment((-57,21)).segment((-63,21)).close().assemble().finalize().extrude(-200)