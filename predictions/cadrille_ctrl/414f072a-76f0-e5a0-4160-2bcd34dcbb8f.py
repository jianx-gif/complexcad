import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((21,-22),(22,-20),(24,-18)).arc((22,-19),(21,-22)).assemble().finalize().extrude(-60).union(w0.sketch().circle(30).reset().face(w0.sketch().segment((-11,19),(-10,11)).arc((-14,-2),(-8,-14)).segment((-8,-22)).segment((8,-22)).segment((8,-14)).arc((14,-4),(12,8)).segment((11,16)).close().assemble(),mode='s').push([(25,0)]).circle(6,mode='s').finalize().extrude(60))
