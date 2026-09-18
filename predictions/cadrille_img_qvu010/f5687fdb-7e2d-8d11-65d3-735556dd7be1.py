import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-40,0))
w1=cq.Workplane('YZ',origin=(-71,0,0))
r=w0.sketch().circle(100).circle(89,mode='s').finalize().extrude(60).union(w0.sketch().segment((-67,-61),(98,-1)).arc((-19,88),(-67,-61)).assemble().finalize().extrude(134)).union(w1.sketch().push([(-10,0)]).circle(90).circle(59,mode='s').finalize().extrude(115))