import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-81,29),(-43,-62),(50,-39)).arc((43,-36),(37,-32)).arc((-42,-56),(-74,21)).arc((-78,25),(-81,29)).assemble().finalize().extrude(157).union(w1.sketch().circle(100).circle(97,mode='s').finalize().extrude(64))