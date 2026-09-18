import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-19,13),(38,1),(85,-24)).arc((39,22),(-19,13)).assemble().finalize().extrude(128).union(w1.sketch().arc((-49,-37),(16,-31),(72,-64)).segment((89,-64)).segment((89,-19)).arc((91,-10),(89,-1)).segment((89,34)).segment((86,34)).arc((22,10),(-42,34)).segment((-49,34)).close().assemble().finalize().extrude(-200))