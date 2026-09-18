import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-50,0))
w1=cq.Workplane('ZX',origin=(0,-48,0))
r=w0.sketch().circle(100).circle(97,mode='s').finalize().extrude(-2).union(w0.sketch().arc((-11,-11),(11,-11),(29,0)).segment((29,-4)).segment((34,-4)).segment((34,3)).arc((40,15),(42,29)).close().assemble().finalize().extrude(136)).union(w1.sketch().push([(6,4)]).circle(94).circle(15,mode='s').finalize().extrude(11))