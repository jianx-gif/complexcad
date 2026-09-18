import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-29,29),(28,-29),(29,52)).arc((1,38),(-29,29)).assemble().push([(27,36)]).circle(13,mode='s').finalize().extrude(-200).union(w0.sketch().circle(94).circle(85,mode='s').finalize().extrude(-183)).union(w0.sketch().arc((-95,-40),(93,-34),(-28,96)).arc((-64,38),(-95,-21)).close().assemble().finalize().extrude(-29))