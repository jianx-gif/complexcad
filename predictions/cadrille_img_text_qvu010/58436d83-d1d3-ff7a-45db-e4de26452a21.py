import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,25,0))
w1=cq.Workplane('ZX',origin=(0,96,0))
r=w0.sketch().rect(200,192).circle(65,mode='s').finalize().extrude(-42).union(w1.sketch().arc((-56,12),(-12,10),(18,-23)).arc((39,29),(-13,49)).segment((-13,46)).segment((-18,46)).arc((-40,33),(-56,12)).assemble().finalize().extrude(-192))