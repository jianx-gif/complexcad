import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
w1=cq.Workplane('ZX',origin=(0,50,0))
r=w0.sketch().circle(100).circle(80,mode='s').finalize().extrude(-21).union(w1.sketch().arc((-92,39),(-24,35),(18,-10)).segment((92,-10)).arc((24,59),(-67,55)).segment((-67,55),(-71,55)).segment((-71,53)).arc((-82,47),(-92,39)).assemble().finalize().extrude(-128))