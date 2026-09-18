import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-93))
r=w0.sketch().circle(79).reset().face(w0.sketch().arc((-63,1),(63,-11),(-60,21)).arc((-70,13),(-63,1)).assemble(),mode='s').finalize().extrude(-7).union(w0.sketch().circle(80).reset().face(w0.sketch().arc((-35,52),(31,-55),(-30,55)).segment((-35,55)).close().assemble(),mode='s').finalize().extrude(193))