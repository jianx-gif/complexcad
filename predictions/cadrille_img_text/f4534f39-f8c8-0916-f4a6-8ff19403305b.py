import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((34,13),(3,38),(38,18)).arc((36,16),(34,13)).assemble().finalize().extrude(-189).union(w0.sketch().push([(14,24)]).circle(51).circle(40,mode='s').finalize().extrude(-128)).union(w1.sketch().circle(91).circle(89,mode='s').finalize().extrude(-21))