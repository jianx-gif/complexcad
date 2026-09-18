import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(36,0,0))
r=w0.sketch().arc((-76,-46),(-56,-39),(-38,-29)).arc((-36,-16),(-23,-19)).arc((11,19),(36,-26)).arc((47,-37),(55,-49)).arc((62,-56),(68,-64)).arc((72,-69),(76,-74)).arc((15,68),(-76,-46)).assemble().finalize().extrude(200).union(w1.sketch().arc((-81,-61),(-35,-51),(-1,-82)).segment((67,-82)).segment((67,10)).segment((-81,10)).close().assemble().finalize().extrude(-63))