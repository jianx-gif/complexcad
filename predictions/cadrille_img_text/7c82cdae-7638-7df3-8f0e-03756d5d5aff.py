import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-79,12),(79,12)).arc((0,44),(-79,12)).assemble().finalize().extrude(-200).union(w0.sketch().segment((-80,-44),(-29,-44)).arc((-58,-34),(-80,-14)).close().assemble().finalize().extrude(-63))