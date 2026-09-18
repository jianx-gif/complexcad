import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-12,-26),(12,-26)).segment((12,-25)).arc((27,0),(12,25)).segment((12,26)).segment((-12,26)).segment((-12,25)).arc((-27,0),(-12,-25)).close().assemble().finalize().extrude(-16).union(w0.sketch().circle(50).circle(12,mode='s').finalize().extrude(-8))
