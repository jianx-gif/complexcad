import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-93))
r=w0.workplane(offset=-7/2).cylinder(7,72).union(w0.sketch().circle(80).reset().face(w0.sketch().arc((-63,0),(-69,-22),(-54,-41)).arc((62,19),(-63,0)).assemble(),mode='s').finalize().extrude(193))