import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-50,-25),(38,-25)).segment((38,25)).segment((-50,25)).segment((-50,13)).arc((-47,11),(-50,9)).close().assemble().push([(-6.5,0)]).rect(83,44,mode='s').finalize().extrude(200)