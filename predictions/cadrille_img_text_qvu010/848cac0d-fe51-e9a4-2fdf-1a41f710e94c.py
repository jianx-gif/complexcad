import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-45,0))
w1=cq.Workplane('ZX',origin=(0,-98,0))
r=w0.sketch().arc((-100,36),(-73,-46),(-4,-93)).segment((-4,-100)).segment((4,-100)).segment((4,-93)).arc((54,-80),(89,-46)).arc((-19,-10),(-43,95)).arc((-73,74),(-93,44)).arc((-95,39),(-100,36)).assemble().finalize().extrude(132).union(w1.workplane(offset=196/2).cylinder(196,89))