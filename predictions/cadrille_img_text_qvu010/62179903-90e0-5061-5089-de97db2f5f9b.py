import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().arc((-42,83),(-100,-19),(-20,-99)).segment((-20,-100)).segment((-18,-99)).arc((19,-98),(52,-84)).segment((54,-83)).segment((54,-82)).arc((98,19),(20,99)).segment((20,100)).segment((18,99)).arc((-19,98),(-52,84)).segment((-42,84)).segment((-42,82)).close().assemble().finalize().extrude(154).union(w1.workplane(offset=-5/2).cylinder(5,100))