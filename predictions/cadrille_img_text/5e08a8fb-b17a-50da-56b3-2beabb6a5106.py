import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-38,-39),(38,-39)).segment((38,39)).segment((-38,39)).segment((-38,29)).arc((-34,27),(-38,25)).close().assemble().finalize().extrude(158).union(w1.sketch().segment((-98,-64),(-90,-64)).arc((0,-100),(90,-64)).segment((98,-64)).segment((98,-48)).arc((100,-26),(98,-4)).segment((98,64)).segment((90,64)).arc((0,100),(-90,64)).segment((-98,64)).close().assemble().finalize().extrude(-200))