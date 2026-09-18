import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-80,-13),(79,-13)).segment((79,13)).segment((55,13)).arc((54,11),(53,13)).segment((-80,13)).close().assemble().finalize().extrude(27).union(w0.sketch().segment((53,12),(55,-14)).segment((80,-13)).segment((80,12)).close().assemble().finalize().extrude(200))