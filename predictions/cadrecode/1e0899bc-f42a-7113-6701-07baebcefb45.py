import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(75).reset().face(w0.sketch().arc((-41,-40),(22,-58),(58,0)).arc((-25,57),(-41,-40)).assemble(),mode='s').finalize().extrude(200)