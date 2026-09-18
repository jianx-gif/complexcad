import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
w1=cq.Workplane('XY',origin=(0,0,59))
r=w0.sketch().arc((-94,-36),(-86,-47),(-78,-57)).arc((89,44),(-94,-36)).assemble().finalize().extrude(-147).union(w0.sketch().segment((-26,-28),(26,-28)).segment((26,28)).segment((-26,28)).segment((-26,17)).segment((-23,17)).segment((-23,14)).segment((-26,14)).close().assemble().finalize().extrude(33)).union(w1.sketch().circle(100).circle(94,mode='s').finalize().extrude(-152))