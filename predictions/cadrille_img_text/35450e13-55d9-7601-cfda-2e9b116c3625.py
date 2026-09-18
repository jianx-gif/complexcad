import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('XY',origin=(0,0,91))
r=w0.sketch().push([(0,13)]).circle(13).push([(0,12.5)]).rect(14,17,mode='s').finalize().extrude(134).union(w0.sketch().arc((-1,-1),(0,0),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(138)).union(w1.sketch().segment((-99,-32),(-65,-32)).arc((0,-70),(65,-32)).segment((99,-32)).segment((99,32)).segment((65,32)).arc((0,70),(-65,32)).segment((-99,32)).close().assemble().circle(70,mode='s').finalize().extrude(-191))