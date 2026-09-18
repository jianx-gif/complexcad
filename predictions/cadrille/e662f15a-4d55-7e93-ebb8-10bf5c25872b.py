import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-50,-19),(50,-19)).segment((50,16)).arc((48,17),(46,19)).segment((-46,19)).arc((-48,17),(-50,16)).close().assemble().finalize().extrude(200)