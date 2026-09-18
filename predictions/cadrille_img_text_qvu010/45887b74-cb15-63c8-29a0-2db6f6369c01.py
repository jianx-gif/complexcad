import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().segment((-99,-23),(-63,-23)).segment((-87,46)).segment((-99,46)).close().assemble().reset().face(w0.sketch().segment((-60,46),(-36,-23)).segment((-24,-23)).segment((-24,46)).close().assemble()).finalize().extrude(200).union(w1.sketch().arc((-100,-72),(-86,-56),(-76,-38)).arc((-89,-37),(-100,-34)).close().assemble().finalize().extrude(77))