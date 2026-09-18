import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.sketch().segment((-8,-100),(8,-100)).segment((8,100)).segment((-8,100)).segment((-8,-9)).segment((-4,-9)).segment((-4,-90)).segment((-8,-90)).close().assemble().push([(1.5,45.5)]).rect(7,73,mode='s').finalize().extrude(150)