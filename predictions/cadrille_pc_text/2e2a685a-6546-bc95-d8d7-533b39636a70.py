import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().segment((-20,-100),(-5,-100)).segment((-5,-82)).segment((20,-83)).segment((20,-67)).segment((-5,-68)).segment((-5,100)).segment((-20,100)).close().assemble().push([(-12,24)]).circle(2,mode='s').push([(12.5,-25)]).rect(15,16,mode='s').finalize().extrude(-100)