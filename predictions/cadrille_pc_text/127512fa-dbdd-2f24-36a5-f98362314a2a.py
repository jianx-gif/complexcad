import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().rect(200,150).reset().face(w0.sketch().segment((-86,40),(-37,-13)).segment((-37,-12)).segment((-37,-13)).segment((37,-13)).segment((37,13)).segment((-37,13)).segment((-37,12)).segment((-63,47)).close().assemble(),mode='s').push([(74,36)]).circle(8,mode='s').finalize().extrude(20)