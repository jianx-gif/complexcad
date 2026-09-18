import cadquery as cq
w0=cq.Workplane('YZ',origin=(-50,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.workplane(offset=100/2).cylinder(100,71).union(w1.sketch().segment((-56,-67),(-56,-66)).arc((-87,0),(-56,66)).segment((-56,67)).arc((-100,0),(-56,-67)).assemble().finalize().extrude(200))