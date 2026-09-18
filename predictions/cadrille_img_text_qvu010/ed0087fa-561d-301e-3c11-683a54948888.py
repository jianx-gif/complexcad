import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-35,0))
w1=cq.Workplane('ZX',origin=(0,-89,0))
r=w0.sketch().circle(100).circle(57,mode='s').finalize().extrude(35).union(w1.sketch().arc((-95,30),(89,-46),(-87,50)).arc((-86,48),(-86,46)).arc((85,-45),(-92,30)).close().assemble().finalize().extrude(169))