import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,13)]).circle(12).circle(7,mode='s').finalize().extrude(125).union(w1.sketch().arc((-100,-30),(0,-81),(100,-30)).segment((53,-30)).arc((40,-32),(27,-30)).close().assemble().finalize().extrude(-172))