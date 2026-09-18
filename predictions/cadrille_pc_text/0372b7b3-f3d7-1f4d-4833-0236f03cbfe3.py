import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,90))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-94,-34),(-85,-30),(-76,-28)).arc((89,16),(-78,-34)).close().assemble().finalize().extrude(-136).union(w0.workplane(offset=-44/2).moveTo(0,-1).cylinder(44,80)).union(w1.sketch().push([(0,-1)]).circle(36).circle(27,mode='s').finalize().extrude(-199))