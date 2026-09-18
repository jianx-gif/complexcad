import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,45,0))
w1=cq.Workplane('ZX',origin=(0,94,0))
r=w0.sketch().segment((-89,-89),(89,-89)).segment((89,-21)).segment((-89,10)).close().assemble().finalize().extrude(-26).union(w0.sketch().segment((-100,100),(100,21)).segment((100,89)).segment((53,89)).arc((-24,96),(-100,100)).assemble().finalize().extrude(-19)).union(w1.sketch().arc((-2,-10),(50,-10),(100,-31)).segment((100,-31),(100,-21)).segment((100,-21),(8,-21)).segment((8,-21),(8,-31)).segment((8,-31),(-2,-10)).assemble().finalize().extrude(-188))