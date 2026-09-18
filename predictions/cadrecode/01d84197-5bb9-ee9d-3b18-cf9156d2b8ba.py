import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.workplane(offset=-22/2).cylinder(22,100).union(w0.sketch().circle(100).reset().face(w0.sketch().segment((-89,-38),(-74,-38)).arc((0,-80),(74,-38)).segment((89,-38)).segment((89,38)).segment((74,38)).arc((0,80),(-74,38)).segment((-89,38)).close().assemble(),mode='s').circle(38).finalize().extrude(52))