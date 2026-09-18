import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-28,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,26)]).rect(178,142).circle(55,mode='s').finalize().extrude(11).union(w1.sketch().arc((-96,-30),(0,-80),(96,-30)).segment((68,-30)).arc((0,-75),(-68,-30)).close().assemble().finalize().extrude(-192))