import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.workplane(offset=-37/2).box(8,172,37).union(w0.sketch().circle(87).reset().face(w0.sketch().segment((-62,-4),(-56,-4)).arc((0,-62),(56,-4)).segment((62,-4)).segment((62,4)).segment((56,4)).arc((0,62),(-56,4)).segment((-62,4)).close().assemble(),mode='s').finalize().extrude(26)).union(w1.workplane(offset=-200/2).moveTo(0,-31).box(200,12,200))