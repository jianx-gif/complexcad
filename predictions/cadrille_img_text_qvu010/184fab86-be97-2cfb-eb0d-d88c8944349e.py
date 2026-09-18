import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-37,0))
w1=cq.Workplane('YZ',origin=(-18,0,0))
r=w0.sketch().arc((-100,-16),(12,38),(100,-70)).segment((100,-16)).segment((85,-16)).arc((0,45),(-85,-16)).close().assemble().finalize().extrude(127).union(w1.sketch().arc((-99,-100),(50,-66),(50,78)).arc((23,-47),(-99,-100)).assemble().finalize().extrude(-29))