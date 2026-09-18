import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-49,-34),(-28,16),(-10,74)).arc((-33,23),(-49,-34)).assemble().finalize().extrude(158).union(w1.sketch().arc((-74,-49),(-12,15),(74,20)).arc((-15,33),(-74,-49)).assemble().finalize().extrude(200))