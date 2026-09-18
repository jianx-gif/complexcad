import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-84,-33),(-81,-35),(-81,-39)).arc((83,36),(-84,-33)).assemble().finalize().extrude(-200).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-83))