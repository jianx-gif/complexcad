import cadquery as cq
w0=cq.Workplane('ZX',origin=(-57,100,0))
r=w0.sketch().segment((-53,53),(-47,53)).segment((-47,32)).segment((-32,32)).segment((-32,53)).segment((-26,53)).segment((-26,57)).segment((-32,57)).segment((-32,78)).segment((-47,78)).segment((-47,57)).segment((-53,57)).close().assemble().finalize().extrude(-200)