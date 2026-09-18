import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
w1=cq.Workplane('XY',origin=(0,0,36))
r=w0.sketch().segment((-94,-28),(-90,-28)).arc((0,-100),(90,-28)).segment((94,-28)).segment((94,28)).segment((90,28)).arc((0,100),(-90,28)).segment((-94,28)).close().assemble().circle(93,mode='s').finalize().extrude(-72).union(w0.sketch().circle(87).rect(110,118,mode='s').finalize().extrude(6)).union(w1.sketch().arc((-90,26),(-93,-10),(-79,-44)).arc((92,17),(-89,30)).arc((-89,28),(-90,26)).assemble().finalize().extrude(-87))