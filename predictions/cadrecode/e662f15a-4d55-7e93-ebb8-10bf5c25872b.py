import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-50,-19),(50,-19)).segment((50,15)).segment((47,19)).segment((-47,19)).arc((-48,18),(-50,16)).close().assemble().finalize().extrude(-200)