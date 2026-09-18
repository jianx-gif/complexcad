import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-5))
r=w0.sketch().circle(56).reset().face(w0.sketch().segment((-27,-12),(-27,12)).arc((-30,0),(-27,-12)).assemble(),mode='s').reset().face(w0.sketch().arc((-26,-13),(0,-28),(26,-13)).close().assemble(),mode='s').reset().face(w0.sketch().segment((-26,13),(26,13)).arc((0,28),(-26,13)).assemble(),mode='s').reset().face(w0.sketch().arc((27,-12),(30,0),(27,12)).close().assemble(),mode='s').finalize().extrude(10)
