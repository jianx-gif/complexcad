import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,15,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-50,50),(50,50)).arc((0,91),(-50,50)).assemble().finalize().extrude(-15).union(w1.sketch().push([(0,9.5)]).rect(100,21).push([(27,7)]).circle(6,mode='s').finalize().extrude(-200))