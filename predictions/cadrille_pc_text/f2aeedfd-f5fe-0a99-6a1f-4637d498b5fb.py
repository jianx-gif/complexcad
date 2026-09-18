import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
r=w0.sketch().segment((-10,-100),(10,-100)).segment((10,99)).arc((0,100),(-10,99)).close().assemble().push([(0,-63)]).circle(5,mode='s').finalize().extrude(50)