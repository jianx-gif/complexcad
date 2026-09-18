import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-40,-20),(-14,-20)).arc((-28,-16),(-40,-6)).close().assemble().finalize().extrude(-15).union(w0.sketch().segment((-39,-11),(-37,-11)).segment((-37,-20)).segment((39,-20)).segment((39,20)).segment((-37,20)).segment((-37,11)).segment((-39,11)).close().assemble().finalize().extrude(-15)).union(w0.workplane(offset=-15/2).moveTo(0,-1).box(80,38,15))
