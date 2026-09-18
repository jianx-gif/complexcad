import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-39,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().push([(18,26)]).circle(50).reset().face(w0.sketch().segment((-19,33),(32,-11)).segment((54,14)).segment((3,58)).close().assemble(),mode='s').finalize().extrude(39).union(w1.sketch().arc((-89,-57),(-55,-71),(-23,-86)).segment((23,-86)).arc((55,-71),(89,-57)).arc((86,-5),(89,47)).arc((55,61),(23,75)).segment((-23,75)).arc((-55,61),(-89,47)).arc((-86,-5),(-89,-57)).assemble().finalize().extrude(-185))