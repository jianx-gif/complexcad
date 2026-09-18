import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-64))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-79,-4),(-67,-4)).arc((0,-67),(67,-4)).segment((79,-4)).segment((79,4)).segment((67,4)).arc((0,67),(-67,4)).segment((-79,4)).close().assemble(),mode='s').finalize().extrude(102).union(w0.workplane(offset=128/2).cylinder(128,46))