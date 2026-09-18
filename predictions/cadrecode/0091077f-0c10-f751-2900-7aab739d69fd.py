import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-22,-4),(-16,-4)).segment((-16,-25)).segment((-3,-25)).segment((22,0)).segment((-3,25)).segment((-16,25)).segment((-16,-1)).close().assemble().push([(-12.5,7.5)]).rect(5,1,mode='s').finalize().extrude(-200)