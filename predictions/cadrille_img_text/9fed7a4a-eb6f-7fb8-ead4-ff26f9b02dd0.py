import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-70,56),(-69,57),(-67,57)).arc((-69,58),(-70,56)).assemble().finalize().extrude(197).union(w1.sketch().push([(3,0)]).circle(97).circle(93,mode='s').finalize().extrude(174))