import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-55,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-25,-29),(57,-33)).segment((62,63)).segment((-20,67)).close().assemble().push([(18.5,17)]).rect(77,64,mode='s').finalize().extrude(10).union(w1.sketch().segment((-100,-87),(-74,-87)).arc((0,-100),(74,-87)).segment((100,-87)).segment((100,87)).segment((74,87)).arc((0,100),(-74,87)).segment((-100,87)).close().assemble().finalize().extrude(200))