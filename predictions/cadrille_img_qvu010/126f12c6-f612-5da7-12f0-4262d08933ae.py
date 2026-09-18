import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(-15,-10)]).circle(25).circle(23,mode='s').finalize().extrude(162).union(w0.sketch().segment((-67,-16),(84,-26)).segment((85,-19)).segment((-66,-9)).close().assemble().finalize().extrude(165)).union(w1.sketch().segment((-97,-81),(-89,-81)).arc((-87,-79),(-85,-81)).segment((76,-81)).arc((77,-79),(78,-81)).segment((97,-81)).segment((97,-78)).segment((-97,-78)).close().assemble().finalize().extrude(200))