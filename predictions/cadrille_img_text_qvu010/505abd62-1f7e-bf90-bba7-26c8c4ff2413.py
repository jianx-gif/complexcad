import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('ZX',origin=(0,40,0))
r=w0.sketch().segment((-100,100),(100,-100)).arc((29,19),(-100,100)).assemble().finalize().extrude(-128).union(w1.sketch().circle(96).circle(85,mode='s').finalize().extrude(-139))