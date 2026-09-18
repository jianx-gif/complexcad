import cadquery as cq
w0=cq.Workplane('YZ',origin=(-92,0,0))
w1=cq.Workplane('ZX',origin=(0,-94,0))
r=w0.sketch().segment((-1,-100),(1,-100)).segment((1,-99)).segment((3,-99)).segment((3,-100)).segment((25,-100)).arc((39,-92),(54,-87)).arc((28,-83),(1,-73)).segment((1,-72)).arc((-1,-86),(-1,-100)).assemble().finalize().extrude(192).union(w1.sketch().arc((-38,-74),(-10,-83),(18,-86)).arc((10,-82),(3,-77)).arc((-18,-79),(-38,-74)).assemble().finalize().extrude(123))