import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-22,-5),(-16,-5)).segment((-16,-25)).segment((-2,-25)).segment((22,0)).segment((-3,25)).segment((-16,25)).segment((-16,12)).segment((-22,12)).close().assemble().finalize().extrude(-200)